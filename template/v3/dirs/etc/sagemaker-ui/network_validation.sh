#!/bin/bash
set -eux 

# Input parameters with defaults:
# Default to 1 (Git storage) if no parameter is passed.
is_s3_storage=${1:-"1"}
# Output file path for unreachable services JSON 
network_validation_file=${2:-"/tmp/.network_validation.json"}

# Function to write unreachable services to a JSON file
write_unreachable_services_to_file() {
    local value="$1"
    local file="$network_validation_file"

    # Create the file if it doesn't exist
    if [ ! -f "$file" ]; then
        touch "$file" || {
            echo "Failed to create $file" >&2
            return 0
        }
    fi

    # Check file is writable
    if [ ! -w "$file" ]; then
        echo "Error: $file is not writable" >&2
        return 0
    fi

    # Write JSON object with UnreachableServices key and the comma-separated list value
    jq -n --arg value "$value" '{"UnreachableServices": $value}' > "$file"
}

# Configure AWS CLI region using environment variable REGION_NAME
aws configure set region "${REGION_NAME}"
echo "Successfully configured region to ${REGION_NAME}"

# Metadata file location containing DataZone info
sourceMetaData=/opt/ml/metadata/resource-metadata.json

# Extract necessary DataZone metadata fields via jq
dataZoneDomainId=$(jq -r '.AdditionalMetadata.DataZoneDomainId' < "$sourceMetaData")
dataZoneProjectId=$(jq -r '.AdditionalMetadata.DataZoneProjectId' < "$sourceMetaData")
dataZoneEndPoint=$(jq -r '.AdditionalMetadata.DataZoneEndpoint' < "$sourceMetaData")
dataZoneDomainRegion=$(jq -r '.AdditionalMetadata.DataZoneDomainRegion' < "$sourceMetaData")
s3Path=$(jq -r '.AdditionalMetadata.ProjectS3Path' < "$sourceMetaData")

# Extract bucket name, fallback to empty string if not found
s3ValidationBucket=$(echo "${s3Path:-}" | sed -E 's#s3://([^/]+).*#\1#')

# Call AWS CLI list-connections, including endpoint if specified
if [ -n "$dataZoneEndPoint" ]; then
    response=$(aws datazone list-connections \
        --endpoint-url "$dataZoneEndPoint" \
        --domain-identifier "$dataZoneDomainId" \
        --project-identifier "$dataZoneProjectId" \
        --region "$dataZoneDomainRegion")
else
    response=$(aws datazone list-connections \
        --domain-identifier "$dataZoneDomainId" \
        --project-identifier "$dataZoneProjectId" \
        --region "$dataZoneDomainRegion")
fi

# Extract each connection item as a compact JSON string
connection_items=$(echo "$response" | jq -c '.items[]')

# Required AWS Services for Compute connections and Git
# Initialize SERVICE_COMMANDS with always-needed STS and S3 checks
declare -A SERVICE_COMMANDS=(
  ["STS"]="aws sts get-caller-identity"
  ["S3"]="aws s3api list-objects --bucket \"$s3ValidationBucket\" --max-items 1"
)

# Track connection types found for conditional checks
declare -A seen_types=()

# Iterate over each connection to populate service commands conditionally
while IFS= read -r item; do
  # Extract connection type
  type=$(echo "$item" | jq -r '.type')
  seen_types["$type"]=1

  # For SPARK connections, check for Glue and EMR properties
  if [[ "$type" == "SPARK" ]]; then
    # If sparkGlueProperties present, add Glue check
    if echo "$item" | jq -e '.props.sparkGlueProperties' > /dev/null; then
      SERVICE_COMMANDS["Glue"]="aws glue get-databases --max-items 1"
    fi

    # Check for emr-serverless in sparkEmrProperties.computeArn for EMR Serverless check
    emr_arn=$(echo "$item" | jq -r '.props.sparkEmrProperties.computeArn // empty')
    if [[ "$emr_arn" == *"emr-serverless"* && "$emr_arn" == *"/applications/"* ]]; then
      # Extract the application ID from the ARN
      emr_app_id=$(echo "$emr_arn" | sed -E 's#.*/applications/([^/]+)#\1#')

      # Only set the service command if the application ID is valid
      if [[ -n "$emr_app_id" ]]; then
        SERVICE_COMMANDS["EMR Serverless"]="aws emr-serverless get-application --application-id \"$emr_app_id\""
      fi
    fi
  fi
done <<< "$connection_items"

# Add Athena if ATHENA connection found
[[ -n "${seen_types["ATHENA"]}" ]] && SERVICE_COMMANDS["Athena"]="aws athena list-data-catalogs --max-items 1"

# Add Redshift checks if REDSHIFT connection found
if [[ -n "${seen_types["REDSHIFT"]}" ]]; then
  SERVICE_COMMANDS["Redshift Clusters"]="aws redshift describe-clusters --max-records 20"
  SERVICE_COMMANDS["Redshift Serverless"]="aws redshift-serverless list-namespaces --max-results 1"
fi

# If using Git Storage (S3 storage flag == 1), check CodeConnections connectivity
# Domain Execution role contains permissions for CodeConnections
if [[ "$is_s3_storage" == "1" ]]; then
  SERVICE_COMMANDS["CodeConnections"]="aws codeconnections list-connections --max-results 1 --profile DomainExecutionRoleCreds"
fi

# Timeout (seconds) for each API call
api_time_out_limit=10
# Array to accumulate unreachable services
unreachable_services=()
# Create a temporary directory to store individual service results
temp_dir=$(mktemp -d)

# Launch all service API checks in parallel background jobs
for service in "${!SERVICE_COMMANDS[@]}"; do
  {
    output_file="$temp_dir/${service}_output"

    # Run command with timeout
    if timeout "${api_time_out_limit}s" bash -c "${SERVICE_COMMANDS[$service]}" > "$output_file" 2>&1; then
      # Success: write OK to temp file
      echo "OK" > "$temp_dir/$service"
    else
      # Get exit code to differentiate timeout or other errors
      exit_code=$?
      if grep -q "Could not connect to the endpoint URL" "$output_file"; then
        echo "UNREACHABLE" > "$temp_dir/$service"
      elif [ "$exit_code" -eq 124 ]; then
        # Timeout exit code
        echo "TIMEOUT" > "$temp_dir/$service"
      else
        # Other errors (e.g., permission denied)
        echo "ERROR" > "$temp_dir/$service"
      fi
    fi
  } &
done

# Wait for all background jobs to complete before continuing
wait

# Process each service's result file to identify unreachable ones
for service in "${!SERVICE_COMMANDS[@]}"; do
  result_file="$temp_dir/$service"
  if [ -f "$result_file" ]; then
    result=$(<"$result_file")
    if [[ "$result" == "TIMEOUT" ]]; then
      echo "$service API did NOT resolve within ${api_time_out_limit}s. Marking as unreachable."
      unreachable_services+=("$service")
    elif [[ "$result" == "UNREACHABLE" ]]; then
      echo "$service API failed to connect to the endpoint. Marking as unreachable."
      unreachable_services+=("$service")
    elif [[ "$result" == "OK" ]]; then
      echo "$service API is reachable."
    else
      echo "$service API returned an error (but not a timeout or endpoint reachability failure). Ignored for network check."
    fi
  else
    echo "$service check did not produce a result file. Skipping."
  fi
done

# Cleanup temporary directory
rm -rf "$temp_dir"

# Write unreachable services to file if any, else write empty string
if (( ${#unreachable_services[@]} > 0 )); then
  joined_services=$(IFS=','; echo "${unreachable_services[*]}")
  # Add spaces after commas for readability
  joined_services_with_spaces=${joined_services//,/,\ }
  write_unreachable_services_to_file "$joined_services_with_spaces"
  echo "Unreachable AWS Services: ${joined_services_with_spaces}"
else
  write_unreachable_services_to_file ""
  echo "All required AWS services reachable within ${api_time_out_limit}s"
fi
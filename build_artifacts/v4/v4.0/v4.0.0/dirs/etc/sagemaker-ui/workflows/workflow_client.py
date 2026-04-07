import argparse

import boto3


def check_blueprint(region: str, domain_id: str, endpoint: str, project_id: str, **kwargs):
    DZ_CLIENT = boto3.client("datazone")
    # add correct endpoint for gamma env
    if endpoint != "":
        DZ_CLIENT = boto3.client("datazone", endpoint_url=endpoint)
    try:
        # check if workflows blueprint is enabled in project profile
        project_profile_id = DZ_CLIENT.get_project(domainIdentifier=domain_id, identifier=project_id)[
            "projectProfileId"
        ]
        project_blueprints = DZ_CLIENT.get_project_profile(domainIdentifier=domain_id, identifier=project_profile_id)[
            "environmentConfigurations"
        ]
        proj_blueprint_ids = [proj_env_config["environmentBlueprintId"] for proj_env_config in project_blueprints]
        blueprint_id = DZ_CLIENT.list_environment_blueprints(
            managed=True, domainIdentifier=domain_id, name="Workflows"
        )["items"][0]["id"]

        if blueprint_id in proj_blueprint_ids:
            blueprint_config = DZ_CLIENT.get_environment_blueprint_configuration(
                domainIdentifier=domain_id, environmentBlueprintIdentifier=blueprint_id
            )
            enabled_regions = blueprint_config["enabledRegions"]
            print(str(region in enabled_regions))
        else:
            print("False")
    except:
        # fallback to checking if only workflows blueprint exists
        try:
            blueprint_id = DZ_CLIENT.list_environment_blueprints(
                managed=True, domainIdentifier=domain_id, name="Workflows"
            )["items"][0]["id"]
            blueprint_config = DZ_CLIENT.get_environment_blueprint_configuration(
                domainIdentifier=domain_id, environmentBlueprintIdentifier=blueprint_id
            )
            enabled_regions = blueprint_config["enabledRegions"]
            print(str(region in enabled_regions))
        except:
            print("False")


COMMAND_REGISTRY = {
    "check-blueprint": check_blueprint,
}


def main():
    parser = argparse.ArgumentParser(description="Workflow blueprint checker")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    check_blueprint_parser = subparsers.add_parser("check-blueprint", help="Check Workflows blueprint")
    check_blueprint_parser.add_argument(
        "--domain-id", type=str, required=True, help="Datazone Domain ID for blueprint check"
    )
    check_blueprint_parser.add_argument("--region", type=str, required=True, help="Datazone Domain region")
    check_blueprint_parser.add_argument(
        "--endpoint", type=str, required=True, help="Datazone endpoint for blueprint check"
    )
    check_blueprint_parser.add_argument(
        "--project-id", type=str, required=True, help="Datazone Project ID for blueprint check"
    )

    args = parser.parse_args()

    if args.command in COMMAND_REGISTRY:
        COMMAND_REGISTRY[args.command](**vars(args))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

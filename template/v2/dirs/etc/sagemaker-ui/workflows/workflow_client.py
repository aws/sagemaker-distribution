import argparse
from datetime import datetime, timezone
from typing import Optional

import boto3
import requests

JUPYTERLAB_URL = "http://default:8888/jupyterlab/default/"
WORKFLOWS_API_ENDPOINT = "api/sagemaker/workflows"
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S.%f%z"


def _validate_response(function_name: str, response: requests.Response):
    if response.status_code == 200:
        return response
    else:
        raise RuntimeError(f"{function_name} returned {response.status_code}: {str(response.content)}")


def update_local_runner_status(session: requests.Session, status: str, detailed_status: Optional[str] = None, **kwargs):
    response = session.post(
        url=JUPYTERLAB_URL + WORKFLOWS_API_ENDPOINT + "/update-local-runner-status",
        headers={"X-Xsrftoken": session.cookies.get_dict()["_xsrf"]},
        json={
            "timestamp": datetime.now(timezone.utc).strftime(TIMESTAMP_FORMAT),
            "status": status,
            "detailed_status": detailed_status,
        },
    )
    return _validate_response("UpdateLocalRunner", response)


def start_local_runner(session: requests.Session, **kwargs):
    response = session.post(
        url=JUPYTERLAB_URL + WORKFLOWS_API_ENDPOINT + "/start-local-runner",
        headers={"X-Xsrftoken": session.cookies.get_dict()["_xsrf"]},
        json={},
    )
    return _validate_response("StartLocalRunner", response)


def stop_local_runner(session: requests.Session, **kwargs):
    response = session.post(
        url=JUPYTERLAB_URL + WORKFLOWS_API_ENDPOINT + "/stop-local-runner",
        headers={"X-Xsrftoken": session.cookies.get_dict()["_xsrf"]},
        json={},
    )
    return _validate_response("StopLocalRunner", response)


def check_blueprint(region: str, domain_id: str, endpoint: str, **kwargs):
    DZ_CLIENT = boto3.client("datazone")
    # add correct endpoint for gamma env
    if endpoint != "":
        DZ_CLIENT = boto3.client("datazone", endpoint_url=endpoint)
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
    "update-local-runner-status": update_local_runner_status,
    "start-local-runner": start_local_runner,
    "stop-local-runner": stop_local_runner,
    "check-blueprint": check_blueprint,
}


def main():
    parser = argparse.ArgumentParser(description="Workflow local runner client")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    update_status_parser = subparsers.add_parser("update-local-runner-status", help="Update status of local runner")
    update_status_parser.add_argument("--status", type=str, required=True, help="Status to update")
    update_status_parser.add_argument("--detailed-status", type=str, required=False, help="Detailed status text")

    start_parser = subparsers.add_parser("start-local-runner", help="Start local runner")

    stop_parser = subparsers.add_parser("stop-local-runner", help="Stop local runner")

    check_blueprint_parser = subparsers.add_parser("check-blueprint", help="Check Workflows blueprint")
    check_blueprint_parser.add_argument(
        "--domain-id", type=str, required=True, help="Datazone Domain ID for blueprint check"
    )
    check_blueprint_parser.add_argument("--region", type=str, required=True, help="Datazone Domain region")
    check_blueprint_parser.add_argument(
        "--endpoint", type=str, required=True, help="Datazone endpoint for blueprint check"
    )

    args = parser.parse_args()

    # create the request session
    session = requests.Session()
    # populate XSRF cookie
    session.get(JUPYTERLAB_URL)

    kwargs = vars(args) | {"session": session}

    if args.command in COMMAND_REGISTRY:
        COMMAND_REGISTRY[args.command](**kwargs)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

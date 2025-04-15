import argparse
from typing import Optional
import requests
from datetime import datetime, timezone

JUPYTERLAB_URL = "http://default:8888/jupyterlab/default/"
WORKFLOWS_API_ENDPOINT = "api/sagemaker/workflows"
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S.%f%z"

def _validate_response(function_name: str, response: requests.Response):
    if response.status_code == 200:
        return response
    else:
        raise RuntimeError(
            f"{function_name} returned {response.status_code}: {str(response.content)}"
        )


def update_local_runner_status(
    session: requests.Session, status: str, detailed_status: Optional[str] = None, **kwargs
):
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

COMMAND_REGISTRY = {
    "update-local-runner-status": update_local_runner_status,
    "start-local-runner": start_local_runner,
    "stop-local-runner": stop_local_runner
}

def main():
    parser = argparse.ArgumentParser(description="Workflow local runner client")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    update_status_parser = subparsers.add_parser(
        "update-local-runner-status", help="Update status of local runner"
    )
    update_status_parser.add_argument("--status", type=str, required=True, help="Status to update")
    update_status_parser.add_argument(
        "--detailed-status", type=str, required=False, help="Detailed status text"
    )

    start_parser = subparsers.add_parser("start-local-runner", help="Start local runner")

    stop_parser = subparsers.add_parser("stop-local-runner", help="Stop local runner")

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

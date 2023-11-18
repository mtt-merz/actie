import json
from os.path import join as join_paths
from os import getcwd
import requests

# For references about OpenWhisk REST API
# https://petstore.swagger.io/?url=https://raw.githubusercontent.com/openwhisk/openwhisk/master/core/controller/src/main/resources/apiv1swagger.json


class OpenWhisk:
    def __init__(self, api_host: str, auth: str) -> None:
        self.api_host = api_host
        self.auth = auth.split(":")
        self.namespace = "_"

    def init() -> "OpenWhisk":
        with open(join_paths(getcwd(), "config.json"), "r") as f:
            config = json.loads(f.read())["wsk"]

        return OpenWhisk(config["host"], config["auth"])

    def create(self, action_name: str, code: str) -> dict:
        res = requests.put(
            f"{self.api_host}/api/v1/namespaces/{self.namespace}/actions/{action_name}",
            auth=(self.auth[0], self.auth[1]),
            headers={
                "content-type": "application/json"
            },
            params={
                "result": True,
            },
            json={
                "namespace": self.namespace,
                "name": action_name,
                "exec": {
                    "kind": "python:3.10",
                    "code": code,
                    "binary": True
                },
                "annotations": [{
                    "key": "provide-api-key",
                    "value": True
                }]
            }
        )

        return json.loads(res.content)

    def invoke(self, action_name: str, actor_name: str, message: str, result: bool = False) -> None:
        res = requests.post(
            f"{self.api_host}/api/v1/namespaces/{self.namespace}/actions/{action_name}?blocking={result}&result={result}",
            auth=(self.auth[0], self.auth[1]),
            headers={
                "content-type": "application/json"
            },
            # params={
            #     "result": True,
            # },
            json={
                "actor_name": actor_name,
                # "actor_family": action_name,
                "message": message,
            },
        )

        res = json.loads(res.content)
        print(json.dumps(res, indent=2))

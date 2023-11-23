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

    def create(self, action: str, code: str) -> dict:
        res = requests.put(
            f"{self.api_host}/api/v1/namespaces/{self.namespace}/actions/{action}",
            auth=(self.auth[0], self.auth[1]),
            headers={
                "content-type": "application/json"
            },
            params={
                "overwrite": True,
            },
            json={
                "namespace": self.namespace,
                "name": action,
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

    def invoke(self, action: str, body: dict, result: bool = False) -> dict:
        res = requests.post(
            f"{self.api_host}/api/v1/namespaces/{self.namespace}/actions/{action}",
            auth=(self.auth[0], self.auth[1]),
            headers={
                "content-type": "application/json"
            },
            params={
                "blocking": result,
                "result": result,
            },
            json=body,
        )

        return json.loads(res.content)

    def invoke_actor(self, family: str, name: str, message: dict, result: bool = False) -> dict:
        return self.invoke(
            action=family,
            body={
                "actor_name": name,
                "message": message,
            },
            result=result,
        )


def init_openwhisk() -> OpenWhisk:
    with open(join_paths(getcwd(), "config.json"), "r") as f:
        config = json.loads(f.read())["wsk"]

    return OpenWhisk(config["host"], config["auth"])

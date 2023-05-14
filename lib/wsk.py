import json
import requests

# For references about OpenWhisk REST API
# https://petstore.swagger.io/?url=https://raw.githubusercontent.com/openwhisk/openwhisk/master/core/controller/src/main/resources/apiv1swagger.json


class OpenWhisk:
    def __init__(self, api_host: str, auth: str) -> None:
        self.api_host = api_host
        self.auth = auth.split(":")
        self.namespace = "_"

    def create(self, name: str, code: str) -> dict:

        res = requests.put(
            f"{self.api_host}/api/v1/namespaces/{self.namespace}/actions/{name}",
            auth=(self.auth[0], self.auth[1]),
            headers={
                "content-type": "application/json"
            },
            params={
                "result": True,
            },
            json={
                "namespace": self.namespace,
                "name": name,
                "exec": {
                    "kind": "python:3",
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

    def invoke(self, name: str, id: str, message: str) -> None:
        res = requests.post(
            f"{self.api_host}/api/v1/namespaces/{self.namespace}/actions/{name}",
            auth=(self.auth[0], self.auth[1]),
            headers={
                "content-type": "application/json"
            },
            params={
                "result": True,
            },
            json={
                "actor_id": id,
                "actor_type": name,
                "message": message,
            },
        )

        res = json.loads(res.content)
        print(json.dumps(res, indent=2))

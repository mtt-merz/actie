import json
import os
import requests


# For references about OpenWhisk REST API
# https://petstore.swagger.io/?url=https://raw.githubusercontent.com/openwhisk/openwhisk/master/core/controller/src/main/resources/apiv1swagger.json

class OpenWhiskAPI:
    def __init__(self):
        # Load config
        config = open(os.path.join(
            os.getcwd(), "actie", "config.json"), "r").read()
        config = json.loads(config)

        self.api_host = config["api_host"]
        self.auth = config["auth"].split(":")
        self.namespace = "_"

    def create(self, name: str, code: bytes) -> None:
        res = requests.put(
            f"{self.api_host}/api/v1/namespaces/{self.namespace}/actions/{name}",
            auth=(self.auth[0], self.auth[1]),
            headers={
                "content-type": "application/json"
            },
            params={
                "overwrite": 'true',
                "result": 'true'
            },
            json={
                "namespace": self.namespace,
                "name": name,
                "exec": {
                    "kind": "python:3",
                    "code": str(code)
                }
            }
        )
        
        print(res.content)

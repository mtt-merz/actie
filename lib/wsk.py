import json
from os.path import join as join_paths
from os import getcwd
import requests
from subprocess import run
import sys

# For references about OpenWhisk REST API
# https://petstore.swagger.io/?url=https://raw.githubusercontent.com/openwhisk/openwhisk/master/core/controller/src/main/resources/apiv1swagger.json


class OpenWhiskInterface:
    def create(self, name: str, code: str) -> dict:
        pass

    def invoke(self, name: str, id: str, message: str) -> None:
        pass


class OpenWhisk(OpenWhiskInterface):
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


class LocalOpenWhisk(OpenWhiskInterface):
    def create(self, name: str, code: str) -> dict:
        pass

    def invoke(self, name: str, id: str, message: str) -> None:
        path = join_paths(getcwd(), "build", name)
        if path not in sys.path:
            sys.path.append(path)

        with open(join_paths(path,  "__main__.py"), "r") as f:
            args = {
                "actor_id": id,
                "message": message,
                "isolate": False,
                "persist": True
            }

            # Invoke "main" with specified args, then print result
            code = f.read()
            code = code + f"res = main({args})\nprint(res)"

            compiled_code = compile(code, "<string>", "exec")
            exec(compiled_code, globals())


def get_wsk(local: bool) -> OpenWhiskInterface:
    if (local):
        return LocalOpenWhisk()

    else:
        with open(join_paths(getcwd(), "config.json"), "r") as f:
            config = json.loads(f.read())["wsk"]

        return OpenWhisk(config["host"], config["auth"])

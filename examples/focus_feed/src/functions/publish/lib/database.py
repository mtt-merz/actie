import json
from os import getcwd
from os.path import join as join_paths
import requests


class Database:
    def __init__(self):
        with open(join_paths(getcwd(), "config.json"), "r") as f:
            config = json.loads(f.read())["database"]

        self.api_host = config["host"]

    def get(self, table: str) -> list[dict]:
        res = requests.get(
            f"{self.api_host}/{table}"
        )

        return json.loads(res.content)

    def post(self, table: str, body: dict) -> dict:
        res = requests.post(
            f"{self.api_host}/{table}",
            headers={
                "Content-Type": "application/json",
            },
            json=body,
        )

        return json.loads(res.content)

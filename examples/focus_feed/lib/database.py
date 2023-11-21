import json
from os import getcwd
from os.path import join as join_paths
import requests


class Database:
    def __init__(self):
        with open(join_paths(getcwd(), "config.json"), "r") as f:
            config = json.loads(f.read())["database"]

        self.api_host = config["host"]

    def get(self, table: str, id: str | None = None) -> list[dict]:
        res = requests.get(
            f"{self.api_host}/{table}{'' if id is None else f'/{id}'}",
        )

        return json.loads(res.content)

    def post(self, table: str, body: dict, id: str | None = None) -> dict:
        res = requests.post(
            f"{self.api_host}/{table}{'' if id is None else f'/{id}'}",
            headers={
                "Content-Type": "application/json",
            },
            json=body,
        )

        return json.loads(res.content)

    def delete(self, table: str, id: str) -> dict:
        res = requests.delete(
            f"{self.api_host}/{table}/{id}",
        )

        return json.loads(res.content)

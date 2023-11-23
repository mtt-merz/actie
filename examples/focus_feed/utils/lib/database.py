import json
from os import getcwd
from os.path import join as join_paths
import requests


class Database:
    def __init__(self):
        with open(join_paths(getcwd(), "config.json"), "r") as f:
            config = json.loads(f.read())["database"]

        self.api_host = config["host"]

    def create(self, path: str, body: dict = {}) -> None:
        res = requests.post(
            url=f"{self.api_host}/{path}",
            headers={
                "Content-Type": "application/json",
            },
            json=body,
        )

        if not res.ok:
            raise Exception(f"Error: {res.status_code} - {res.content}")

    def read(self, path: str, query: dict[str, str] = {}) -> list[dict]:
        res = requests.get(
            url=f"{self.api_host}/{path}",
            params=query
        )

        if not res.ok:
            raise Exception(f"Error: {res.status_code} - {res.content}")

        return json.loads(res.content)

    def update(self, path: str, body: dict = {}, query: dict[str, str] = {}) -> None:
        res = requests.patch(
            url=f"{self.api_host}/{path}",
            headers={
                "Content-Type": "application/json",
            },
            json=body,
            params=query,
        )

        if not res.ok:
            raise Exception(f"Error: {res.status_code} - {res.content}")

    def delete(self, path: str, query: dict[str, str] = {}) -> None:
        res = requests.delete(
            url=f"{self.api_host}/{path}",
            params=query
        )

        if not res.ok:
            raise Exception(f"Error: {res.status_code} - {res.content}")

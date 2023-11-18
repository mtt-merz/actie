import requests
import json
from os.path import join as join_paths
from os import getcwd
import requests
import traceback

from lib import init_openwhisk


class Database:
    def __init__(self):
        self.api_host = "https://344d-2a01-e11-1402-c210-7d3-be71-a749-ef75.ngrok.io"

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


def main(args) -> dict:
    try:
        topic = args['message']['topic']
        content = args['message']['content']

        db = Database()

        # add content to contents table
        db.post('contents', {})

        # get subscribers from subscriptions table
        subscribers = db.get('subscribers')

        # call aggregate for each subriber
        wsk = init_openwhisk()
        for subscriber in subscribers:
            wsk.invoke


        result = db.get("todos")

        return {"elements": result}

    except Exception:
        return {
            "error": traceback.format_exc()
        }

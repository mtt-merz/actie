import json
import time
import traceback

from lib.database import Database
from lib.wsk import init_openwhisk


def main(args) -> dict:
    try:
        topic = args['topic']
        article = args['article']

        db = Database()

        # add article to articles table
        db.create(
            path='articles',
            body={
                "topic": topic,
                "body": article,
                "published": round(time.time() * 1000),
            }
        )

        # get subscribers from subscriptions table
        subscribers: list[dict] = db.read(
            path='subscriptions',
            query={
                'topic': f'eq.{topic}'
            },
        )
        print(subscribers)

        # call aggregate for each subriber
        wsk = init_openwhisk()
        for subscriber in subscribers:
            wsk.invoke('aggregate', {
                "topic": topic,
                "user": subscriber["user_name"],
            })

        return {
            "result": f"Article '{article}' published in topic '{topic}'"
        }

    except Exception:
        return {
            "error": traceback.format_exc()
        }


def test():
    result = main({
        "topic": "tech",
        "article": "ciriciao",
    })

    print(json.dumps(result, indent=2))

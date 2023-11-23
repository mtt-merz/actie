import json
import traceback

from lib.database import Database


def main(args) -> dict:
    try:
        topic = args['topic']
        user = args['user']
        policy = args.get('policy')

        db = Database()

        # check if user already subscribed
        subscriptions: list[dict] = db.read(
            path='subscriptions',
            query={
                'topic': f'eq.{topic}',
                'user_name': f'eq.{user}'
            })

        if len(subscriptions) > 0:
            return {
                "result": f"User '{user}' already subscribed to topic '{topic}'"
            }

        # add to subscriptions table
        db.create('subscriptions', {
            "user_name": user,
            "topic": topic,
            "user_policy": policy or 1,
            "last_published": 0,
        })

        return {
            "result": f"User '{user}' subscribed to topic '{topic}'"
        }

    except Exception:
        return {
            "error": traceback.format_exc()
        }


def test():
    res = main({
        "topic": "tech1",
        "user": "marco",
    })

    print(json.dumps(res, indent=2))

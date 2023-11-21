import traceback

from lib.database import Database


def main(args) -> dict:
    try:
        topic = args['topic']
        user = args['user']
        policy = args.get('policy')

        db = Database()

        # check if user already subscribed
        for subscription in db.get('subscriptions'):
            if subscription['topic'] == topic and subscription['user'] == user:
                return {
                    "result": f"User '{user}' already subscribed to topic '{topic}'"
                }

        # add to subscriptions table
        db.post('subscriptions', {
            "topic": topic,
            "user": user,
            "policy": policy or 1,
            "last_published": 0,
        })

        return {
            "result": f"User '{user}' subscribed to topic '{topic}'"
        }

    except Exception:
        return {
            "error": traceback.format_exc()
        }

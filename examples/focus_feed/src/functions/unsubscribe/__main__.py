import traceback

from lib.database import Database


def main(args) -> dict:
    try:
        topic = args['topic']
        user = args['user']

        db = Database()

        # get subscription
        subscription: dict | None = None
        for sub in db.get('subscriptions'):
            if sub['topic'] == topic and sub['user'] == user:
                subscription = sub
                break

        # check if user was subscribed
        if subscription is None:
            return {
                "result": f"User '{user}' not subscribed to topic '{topic}'"
            }

        # remove from subscriptions table
        db.delete('subscriptions', subscription["id"])

        return {
            "result": f"User '{user}' unsubscribed from topic '{topic}'"
        }

    except Exception:
        return {
            "error": traceback.format_exc()
        }

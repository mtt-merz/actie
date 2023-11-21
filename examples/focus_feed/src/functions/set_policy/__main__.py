import traceback

from lib.database import Database


def main(args) -> dict:
    try:
        topic = args['topic']
        user = args['user']
        policy = args['policy']

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

        # set policy to subscriptions table
        db.post(
            table='subscriptions',
            id=subscription["id"],
            body={
                "topic": topic,
                "user": user,
                "policy": policy,
            })

        return {
            "result": f"User '{user}' policy set to {policy} for topic '{topic}'"
        }

    except Exception:
        return {
            "error": traceback.format_exc()
        }

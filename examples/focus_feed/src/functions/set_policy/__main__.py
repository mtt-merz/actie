import traceback

from lib.database import Database


def main(args) -> dict:
    try:
        topic = args['topic']
        user = args['user']
        policy = args['policy']

        db = Database()

        # check if user is subscribed
        subcriptions = db.read(
            path='subscriptions',
            query={
                'topic': f'eq.{topic}',
                'user_name': f'eq.{user}'
            }
        )
        if len(subcriptions) == 0:
            return {
                "result": f"User '{user}' not subscribed to topic '{topic}'"
            }

        # set policy to subscriptions table
        db.update(
            path='subscriptions',
            query={
                'topic': f'eq.{topic}',
                'user_name': f'eq.{user}'
            },
            body={
                "policy": policy,
            })

        return {
            "result": f"User '{user}' policy set to {policy} for topic '{topic}'"
        }

    except Exception:
        return {
            "error": traceback.format_exc()
        }

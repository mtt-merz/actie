import traceback

from lib.database import Database


def main(args) -> dict:
    try:
        topic = args['topic']
        user = args['user']

        db = Database()

        # check if user is subscribed
        subscriptions: list[dict] = db.read(
            path='subscriptions',
            query={
                'topic': f'eq.{topic}',
                'user_name': f'eq.{user}'
            })

        if len(subscriptions) == 0:
            return {
                "result": f"User '{user}' not subscribed to topic '{topic}'"
            }

        # remove from subscriptions table
        db.delete(
            path='subscriptions',
            query={
                'topic': f'eq.{topic}',
                'user_name': f'eq.{user}'
            })

        return {
            "result": f"User '{user}' unsubscribed from topic '{topic}'"
        }

    except Exception:
        return {
            "error": traceback.format_exc()
        }

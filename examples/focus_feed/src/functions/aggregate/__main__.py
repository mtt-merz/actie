import traceback

from lib.database import Database


def main(args) -> dict:
    try:
        topic = args['topic']
        user = args['user']

        db = Database()

        # get policy from subscriptions table
        subscriptions: list[dict] = db.read(
            path='subscriptions',
            query={
                'topic': f'eq.{topic}',
                'user_name': f'eq.{user}'
            }
        )
        if len(subscriptions) == 0:
            return {
                "result": f"User '{user}' not subscribed to topic '{topic}'"
            }

        subscription = subscriptions[0]

        policy = subscription["user_policy"]
        last_published = subscription["last_published"]

        # get last topic articles from arcticles table, depending on policy
        articles: list[dict] = db.read(
            path='articles',
            query={
                'topic': f'eq.{topic}',
                'published': f'gt.{last_published}'
            }
        )

        if len(articles) < policy:
            return {"result": f"Topic '{topic}' no aggregation performed for user '{user}':" +
                              f"missing {policy - len(articles)} article(s)"}

        # update last_published timestamp
        articles.sort(key=lambda x: x["published"])
        timestamp = articles[-1]["published"]
        db.update(
            path=f'subscriptions',
            query={
                'user_name': f'eq.{user}',
                'topic': f'eq.{topic}'
            },
            body={
                # "last_published": timestamp,
                "last_published": 0,
            }
        )

        return {
            "result": f"Topic '{topic}' aggregation for user '{user}': {len(articles)} article(s)"
        }

    except Exception:
        return {
            "error": traceback.format_exc()
        }

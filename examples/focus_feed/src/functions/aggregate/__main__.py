import traceback

from lib.database import Database


def main(args) -> dict:
    topic = args['topic']
    user = args['user']

    db = Database()

    # get policy from subscriptions table
    subscription: dict = {}
    for sub in db.get('subscriptions'):
        if sub['topic'] == topic and sub['user'] == user:
            subscription: dict = sub
            break

    policy = subscription["policy"]
    last_published = subscription["last_published"]

    # get last topic contents from contents table, depending on policy
    contents: list[dict] = []
    for content in db.get('contents'):
        if content['topic'] == topic and content['timestamp'] > last_published:
            contents.append(content)

    if len(contents) >= policy:
        # publish contents

        contents.sort(key=lambda x: x["timestamp"])
        last_published_timestamp = contents[-1]["timestamp"]
        db.post(
            table='subscriptions',
            id=subscription["id"],
            body={
                "user": user,
                "topic": topic,
                "policy": policy,
                "last_published": last_published_timestamp,
            }
        )

    return args

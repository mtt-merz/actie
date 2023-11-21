import time
import traceback

from lib.database import Database
from lib.wsk import init_openwhisk


def main(args) -> dict:
    try:
        topic = args['topic']
        content = args['content']

        db = Database()

        # add content to contents table
        db.post(
            table='contents',
            body={
                "topic": topic,
                "content": content,
                "timestamp": round(time.time() * 1000),
            }
        )

        # get subscribers from subscriptions table
        subscribers: list[str] = []
        for subscription in db.get('subscriptions'):
            if subscription['topic'] == topic:
                subscribers.append(subscription['user'])

        # call aggregate for each subriber
        wsk = init_openwhisk()
        for subscriber in subscribers:
            wsk.invoke('aggregate', {
                "topic": topic,
                "user": subscriber,
            })

        return {
            "elements": subscribers,
            "topic": str(topic),
            "content": str(content),
        }

    except Exception:
        return {
            "error": traceback.format_exc()
        }


# {"actor_name": "tech",   "isolate": False, "persist": False,    "message": {"action": "publish",        "args": {"content": {"body": "ciriciao"}}}}

# {'topic':'tech', 'content':'ciriciao'}

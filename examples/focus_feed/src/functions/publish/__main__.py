import traceback

from lib.database import Database
from lib.wsk import init_openwhisk


def main(args) -> dict:
    try:
        topic = args['topic']
        content = args['content']

        db = Database()

        # # add content to contents table
        # db.post('contents', {})

        # # get subscribers from subscriptions table
        # subscribers = db.get('subscribers')

        # # call aggregate for each subriber
        wsk = init_openwhisk()
        # for subscriber in subscribers:
        #     wsk.invoke

        result = db.get("todos")

        return {
            "elements": result,
            "topic": str(topic),
            "content": str(content),
        }

    except Exception:
        return {
            "error": traceback.format_exc()
        }


# {"actor_name": "tech",   "isolate": False, "persist": False,    "message": {"action": "publish",        "args": {"content": {"body": "ciriciao"}}}}

# {'topic':'tech', 'content':'ciriciao'}

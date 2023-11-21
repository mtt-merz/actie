import traceback

from lib.database import Database
from lib.wsk import init_openwhisk

def main(args) -> dict:
    topic = args['topic']
    user = args['user']
    policy = args['policy']

    db = Database()

    # add to subscriptions table
    db.post('subscriptions', {
        "topic": topic,
        "user": user,
        "policy": policy,
        "last_published": 0,
    })

    # call aggregate function
    wsk = init_openwhisk()
    wsk.invoke('aggregate', {
        "topic": topic,
        "user": user,
    })

    return args
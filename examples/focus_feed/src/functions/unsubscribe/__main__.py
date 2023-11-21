import time
import traceback

from lib.database import Database

def main(args) -> dict:
    topic = args['topic']
    user = args['user']

    db = Database()

    # get subscription
    subscription: dict = {}
    for sub in db.get('subscriptions'):
        if sub['topic'] == topic and sub['user'] == user:
            subscription: dict = sub
            break

    # remove from subscriptions table
    db.delete('subscriptions', subscription["id"])
    

    return args
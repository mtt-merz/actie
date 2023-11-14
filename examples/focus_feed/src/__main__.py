import json
import os
import random
from threading import Thread
import time


from lib import OpenWhisk
from utils import Logger


class User:
    def __init__(self, name: str) -> None:
        self.name = name
        self.wsk = OpenWhisk.init()

    def subscribe(self, topic: str, policy: int = 10) -> str:
        def execute(): return self.wsk.invoke(
            'topic', topic,
            json.dumps({
                'action': 'subscribe',
                'args': {
                    'user': self.name,
                    'policy': policy
                }
            }), result=True
        )

        return logger.log(f'subscribe user "{self.name}" to topic "{topic}"', execute)

    def unsubscribe(self, topic: str) -> str:
        def execute(): return self.wsk.invoke(
            'topic', topic,
            json.dumps({
                'action': 'unsubscribe',
                'args': {
                    'user': self.name
                }
            }), result=True
        )

        return logger.log(f'unsubscribe user "{self.name}" from topic "{topic}"', execute)


def publish(topic: str, content: str) -> str:
    wsk = OpenWhisk.init()

    def execute(): return wsk.invoke(
        'topic', topic,
        json.dumps({
            'action': 'publish',
            'args': {
                'content': {'body': content}
            }
        }), result=True
    )

    return logger.log(f'publish content "{content}" to topic "{topic}"', execute)


logger = Logger("test")

mark = User('mark')
annie = User('annie')
frank = User('frank')

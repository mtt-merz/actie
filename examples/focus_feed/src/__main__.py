import json
import os
import random
from threading import Thread
import time

from lib import OpenWhisk


class User:
    def __init__(self, name: str) -> None:
        self.name = name
        self.wsk = OpenWhisk.init()

    def subscribe(self, topic: str, policy: int = 10) -> str:
        return self.wsk.invoke('topic', topic, json.dumps({
            'action': 'subscribe',
            'args': {
                'user': self.name,
                'policy': policy
            }
        }))

    def unsubscribe(self, topic: str) -> str:
        return self.wsk.invoke('topic', topic, json.dumps({
            'action': 'unsubscribe',
            'args': {
                'user': self.name
            }
        }))


def publish(topic: str, content: str) -> str:
    wsk = OpenWhisk.init()
    return wsk.invoke('topic', topic, json.dumps({
        'action': 'publish',
        'args': {
            'content': {'body': content}
        }
    }))


mark = User('mark')
annie = User('annie')
frank = User('frank')

import json
import os
import random
from threading import Thread
import time

from lib import OpenWhisk

wsk: OpenWhisk


def subscribe(wsk: OpenWhisk, topic: str, policy: int = 10) -> str:
    return wsk.invoke('topic', topic, json.dumps({
        'action': 'subscribe',
        'args': {
            'user': 'annie',
            'policy': policy
        }
    }))


def unsubscribe(wsk: OpenWhisk, topic: str) -> str:
    return wsk.invoke('topic', topic, json.dumps({
        'action': 'unsubscribe',
        'args': {
            'user': 'annie'
        }
    }))


subscribe(wsk, 'news')

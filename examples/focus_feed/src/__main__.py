import json
import os
import random
from threading import Thread
import time

from lib import OpenWhiskInterface

wsk: OpenWhiskInterface


wsk.invoke('user', 'Annie', json.dumps({
    'action': 'join_topic',
    'args': {
        'topic': 'news',
        'policy': 10
    }
}))

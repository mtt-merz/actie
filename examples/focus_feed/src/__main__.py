import json

from lib import init_openwhisk
from utils import Logger


def subscribe(topic: str, user: str, policy: int = 10) -> str:
    wsk = init_openwhisk()

    def execute(): return wsk.invoke(
        'topic', topic,
        json.dumps({
            'action': 'subscribe',
            'args': {
                'user': user,
                'policy': policy
            }
        }), result=True
    )

    return logger.log(f'subscribe user "{user}" to topic "{topic}"', execute)


def unsubscribe(topic: str, user: str) -> str:
    wsk = init_openwhisk()

    def execute(): return wsk.invoke(
        'topic', topic,
        json.dumps({
            'action': 'unsubscribe',
            'args': {
                'user': user
            }
        }), result=True
    )

    return logger.log(f'unsubscribe user "{user}" from topic "{topic}"', execute)


def publish(topic: str, content: str) -> str:
    wsk = init_openwhisk()

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

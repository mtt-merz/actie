from configparser import ConfigParser
from enum import Enum
from sys import implementation

from lib import init_openwhisk
from utils import Logger


class Implementation(Enum):
    ACTORS = 'actors'
    FUNCTIONS = 'functions'


wsk = init_openwhisk()


def subscribe(topic: str, user: str, policy: int = 10) -> str:
    def execute():
        match implementation:
            case Implementation.ACTORS:
                return wsk.invoke_actor(
                    family='topic',
                    name=topic,
                    message={
                        'action': 'subscribe',
                        'args': {
                           'user': user,
                           'policy': policy
                        }
                    },
                    result=True,
                )

            case Implementation.FUNCTIONS:
                return wsk.invoke(
                    action='subscribe',
                    body={
                        'topic': topic,
                        'user': user,
                        'policy': policy,
                    },
                    result=False,
                )

    return logger.log(f'subscribe user "{user}" to topic "{topic}"', execute)


def unsubscribe(topic: str, user: str) -> str:
    def execute():
        match implementation:
            case Implementation.ACTORS:
                return wsk.invoke_actor(
                    family='topic',
                    name=topic,
                    message={
                        'action': 'unsubscribe',
                        'args': {
                            'user': user
                        }
                    },
                    result=True,
                )

            case Implementation.FUNCTIONS:
                return wsk.invoke(
                    action='unsubscribe',
                    body={
                        'topic': topic,
                        'user': user,
                    },
                    result=True,
                )

    return logger.log(f'unsubscribe user "{user}" from topic "{topic}"', execute)


def publish(topic: str, content: str) -> str:
    def execute():
        match implementation:
            case Implementation.ACTORS:
                return wsk.invoke_actor(
                    family='topic',
                    name=topic,
                    message={
                        'action': 'publish',
                        'args': {
                           'content': {'body': content}
                        }
                    },
                    result=True,
                )

            case Implementation.FUNCTIONS:
                return wsk.invoke(
                    action='publish',
                    body={
                        "topic": topic,
                        "content": content,
                    },
                    result=True,
                )

    return logger.log(f'publish content "{content}" to topic "{topic}"', execute)


logger = Logger("test")
implementation = Implementation.ACTORS
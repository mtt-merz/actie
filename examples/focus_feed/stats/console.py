from enum import Enum

from lib import init_openwhisk
from logger import Logger


class Implementation(Enum):
    ACTORS = 'actors'
    FUNCTIONS = 'functions'


class Console:
    def __init__(self,
                 implementation: Implementation,
                 id: int | None = None,) -> None:
        self.implementation = implementation

        self.logger = Logger(
            f"{id if id is not None else 'test'}_{implementation.name}")
        self.wsk = init_openwhisk()

    def subscribe(self, topic: str, user: str, policy: int = 1) -> str:
        return self.__execute(
            label=f'subscribe user "{user}" to topic "{topic}"',
            actor_family='user',
            actor_name=user,
            actor_args={
                'topic': topic,
                'policy': policy,
            },
            function='subscribe',
            function_args={
                'topic': topic,
                'user': user,
                'policy': policy
            }
        )

    def unsubscribe(self, topic: str, user: str) -> str:
        return self.__execute(
            label=f'unsubscribe user "{user}" from topic "{topic}"',
            actor_family='user',
            actor_name=user,
            actor_args={
                'topic': topic,
            },
            function='unsubscribe',
            function_args={
                'topic': topic,
                'user': user
            }
        )

    def publish(self, topic: str, article: str) -> str:
        return self.__execute(
            label=f'publish article "{article}" to topic "{topic}"',
            actor_family='topic',
            actor_name=topic,
            actor_args={
                'article': article
            },
            function='publish',
            function_args={
                'topic': topic,
                'article': article
            }
        )

    def __execute(self,
                  label: str,
                  actor_family: str, actor_name: str,
                  function: str,
                  actor_args: dict,
                  function_args: dict) -> str:
        def execute():
            match self.implementation:
                case Implementation.ACTORS:
                    return self.wsk.invoke_actor(
                        family=actor_family,
                        name=actor_name,
                        message={
                            'action': function,
                            'args': actor_args
                        },
                        result=True,
                    )

                case Implementation.FUNCTIONS:
                    return self.wsk.invoke(
                        action=function,
                        body=function_args,
                        result=True,
                    )

        return self.logger.log(label, execute)

from enum import Enum

from lib import init_openwhisk
from logger import Logger


class Implementation(Enum):
    actie = 'actie'
    base = 'base'


class LogArgs:
    def __init__(self, topics: int, users: int, articles: int,
                 subcriptions: int, persist: bool) -> None:
        self.topics = topics
        self.users = users
        self.articles = articles
        self.subcriptions = subcriptions
        self.persist = persist

    def as_dict(self) -> dict:
        return {
            'topics': self.topics,
            'users': self.users,
            'articles': self.articles,
            'subcriptions': self.subcriptions,
            'persist': self.persist
        }


class Console:
    def __init__(self,
                 implementation: Implementation,
                 name: str | None = None,) -> None:
        self.implementation = implementation

        self.logger = Logger(
            name if name is not None else 'test', implementation.name)
        self.wsk = init_openwhisk()

    def subscribe(self, log_args: LogArgs,
                  topic: str, user: str, policy: int = 1) -> str:
        return self.__execute(
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
            },
            log_args=log_args
        )

    def unsubscribe(self, log_args: LogArgs,
                    topic: str, user: str) -> str:
        return self.__execute(
            actor_family='user',
            actor_name=user,
            actor_args={
                'topic': topic,
            },
            function='unsubscribe',
            function_args={
                'topic': topic,
                'user': user
            },
            log_args=log_args
        )

    def publish(self, log_args: LogArgs,
                topic: str, article: str) -> str:
        return self.__execute(
            actor_family='topic',
            actor_name=topic,
            actor_args={
                'article': article
            },
            function='publish',
            function_args={
                'topic': topic,
                'article': article
            },
            log_args=log_args
        )

    def set_policy(self, log_args: LogArgs,
                   topic: str, user: str, policy: int) -> str:
        return self.__execute(
            actor_family='user',
            actor_name=user,
            actor_args={
                'topic': topic,
                'policy': policy
            },
            function='set_policy',
            function_args={
                'user': user,
                'topic': topic,
                'policy': policy
            },
            log_args=log_args
        )

    def aggregate(self, log_args: LogArgs,
                  topic: str, user: str) -> str:
        return self.__execute(
            actor_family='user',
            actor_name=user,
            actor_args={
                'topic': topic,
            },
            function='set_policy',
            function_args={
                'user': user,
                'topic': topic,
            },
            log_args=log_args
        )

    def __execute(self,
                  actor_family: str, actor_name: str,
                  function: str,
                  actor_args: dict,
                  function_args: dict,
                  log_args: LogArgs) -> str:
        def execute():
            match self.implementation:
                case Implementation.actie:
                    return self.wsk.invoke_actor(
                        family=actor_family,
                        name=actor_name,
                        message={
                            'action': function,
                            'args': actor_args
                        },
                        result=True,
                    )

                case Implementation.base:
                    return self.wsk.invoke(
                        action=function,
                        body=function_args,
                        result=True,
                    )

        return self.logger.log(execute, {
            'action': function,
            'implementation': self.implementation.name,
            **(log_args.as_dict())
        })

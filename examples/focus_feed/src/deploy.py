import json
from os.path import join as join_paths
from os import getcwd

from lib import init_openwhisk


def create_action(name: str) -> dict:
    wsk = init_openwhisk()
    with open(join_paths(getcwd(), f"src/functions/{name}.py"), "r") as f:
        code = f.read()

    return wsk.create(name, code)


for action in ['publish', 'aggregate', 'subscribe', 'unsubscribe']:
    result = create_action(action)
    print(json.dumps(result, indent=2))
    print(f'Action "{action}" deployed\n')

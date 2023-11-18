import json
from os.path import join as join_paths
from os import getcwd

from lib import init_openwhisk


wsk = init_openwhisk()

for action in ['publish', 'aggregate', 'subscribe', 'unsubscribe']:
    path = f"src/functions/{action}.py"
    with open(join_paths(getcwd(), path), "r") as f:
        code = f.read()

    result = wsk.create(action, code)

    print(json.dumps(result, indent=2))
    print(f'Action "{action}" deployed\n')

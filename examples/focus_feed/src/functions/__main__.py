import base64
from distutils.dir_util import copy_tree, remove_tree
from inspect import getabsfile
import json
from os.path import join as join_paths, exists
from os import getcwd, mkdir
from shutil import make_archive, copyfile

import lib
from lib import init_openwhisk


wsk = init_openwhisk()

for action in ['publish', 'aggregate', 'subscribe', 'unsubscribe']:
    print(f"Deploying action '{action}'...")

    action_build_path = join_paths(getcwd(), "src", "functions", action)

    print(f"\n[{action}]")

    print("Moving files...")

    # Move internal libraries
    copy_tree(
        getabsfile(lib).removesuffix("/__init__.py"),
        join_paths(action_build_path, "lib")
    )

    # Move configs
    copyfile(
        join_paths(getcwd(), "config.json"),
        join_paths(action_build_path, "config.json")
    )

    print(f"Actor '{action}' built")

    # Archive all files
    archive_path = make_archive(
        join_paths(action_build_path, action), "zip",
        root_dir=action_build_path
    )

    # Deploy actions
    with open(archive_path, "rb") as f:
        code = base64.b64encode(f.read())
        code = code.decode("utf-8")
        res = wsk.create(action, code)

    if "error" in res.keys():
        if "already exists" in res["error"]:
            print("Action already deployed")
        else:
            raise Exception(res["error"])

    else:
        print("Action deployed")

        code = res["exec"]["code"]
        code = code[:100] + f"...({len(code) - 200} chars dropped)"
        res["exec"]["code"] = code
        print(json.dumps(res, indent=2))

print("All actions deployed")

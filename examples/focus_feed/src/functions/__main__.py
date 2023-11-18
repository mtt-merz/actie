import base64
import json
from os.path import join as join_paths
from os import getcwd
from shutil import make_archive

from lib import init_openwhisk


wsk = init_openwhisk()

for action in ['publish', 'aggregate', 'subscribe', 'unsubscribe']:
    print(f"Deploying action '{action}'...")

    action_build_path = join_paths(getcwd(), "src", "functions", action)

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

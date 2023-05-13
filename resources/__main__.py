import json
from os import open as osopen, fdopen, O_RDWR, O_CREAT, stat, getcwd
from os.path import join as join_paths
import pickle
import requests
import traceback

from lib.actor import get_actor_label
from __actor__ import __Actor__


class Repository:
    def __init__(self, id: str) -> None:
        self.id = id
        self.file_name = f"{get_actor_label(__Actor__, id)}.pkl"

        with open(join_paths(getcwd(), "config.json"), "r") as f:
            host = json.loads(f.read())["storage"]["host"]

        self.url = f"{host}/{self.file_name}"

    def __enter__(self):
        # Open snapshot file (create if not present) in READ and WRITE mode
        self.file = fdopen(
            osopen(self.file_name, O_RDWR | O_CREAT), "rb+")
        return self

    def __exit__(self, *args) -> None:
        self.file.close()

    def load(self) -> __Actor__:
        '''Load the actor instance.

        Check first locally; if nothing is found, check the (remote) object storage.

        Raises
        ------
        requests.RequestException
            if the request to the object storage fails.

        Returns
        -------
        actor: Actor
            the loaded actor instance
        '''
        print("Loading snapshot...")

        if stat(self.file_name).st_size > 0:
            print("Snapshot fetched locally.")
            return pickle.load(self.file)

        print("Snapshot not found locally, trying loading from remote...")
        response = requests.get(self.url)

        # TODO: remove check on response content
        if (response.ok and len(response.content) > 0):
            print("Snaphsot loaded remotely.")
            # raise(Exception(f"{response.status_code} - {response.content}"))
            return pickle.loads(response.content)

        if not response.ok and response.status_code != 404:
            raise requests.RequestException(
                f"Fail fetching snapshot from object storage\n{response.content}")

        print("Snapshot neither found remotely: initialize actor")
        return __Actor__(self.id)

    def dump(self, obj: __Actor__, remote: bool) -> None:
        '''Dump the actor instance.

        The dump process is executed first locally.
        The produced file is saved to the object storage iff the "remote" parameter is true.

        Raises
        ------
        requests.RequestException
            if the request to upload self.file fails
        '''
        print("\nDumping snapshot...")

        self.file.seek(0)
        pickle.dump(obj, self.file)
        print("Snapshot dumped locally.")

        if remote:
            self.file.seek(0)
            response = requests.put(self.url, data=self.file.read())

            if not response.ok:
                raise Exception(
                    f"Fail saving snapshot to object storage\n{response.content}")

            print("Snapshot dumped remotely.")


def main(args) -> dict:
    '''Run actor actions in response to messages.

    Attributes
    ----------
    args: dict
        dictionary of parameters to run the right actor actions.

        actor_id: str
            the id of the actor instance
        message: str
            the name of the action to invoke

    Returns
    -------
    out: dict
        the execution results
    '''
    try:
        id = args["actor_id"]
        with Repository(id) as repository:
            actor: __Actor__ = repository.load()

            # Execute code
            msg = args["message"]
            res = actor.receive(msg)

            repository.dump(actor, remote=True)

        return {
            "instance": get_actor_label(__Actor__, id),
            "result": res
        }

    except Exception:
        return {
            "error": traceback.format_exc()
        }


res = main({
    "actor_id": "ASDFG",
    "message": "increment",
})

if "error" in res:
    print(res["error"])
else:
    print(json.dumps(res, indent=2))

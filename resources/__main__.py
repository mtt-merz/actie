import json
from os import open as osopen, fdopen, O_RDWR, O_CREAT, stat, getcwd
from os.path import join as join_paths
import pickle
import requests
import traceback

from lib.actor import get_actor_label
from __actor__ import __Actor__

from lib.wsk import get_wsk


class Source:
    LOCAL = "local",
    REMOTE = "remote",
    NONE = "none"


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

    def load(self) -> tuple:
        '''Load the actor instance.

        Check first locally; if nothing is found, check the (remote) object storage.

        Raises
        ------
        requests.RequestException
            if the request to the object storage fails.

        Returns
        -------
        actor: __Actor__
            the loaded __actor__ instance
        source: Source
            the source of the loaded instance
        '''
        print("Loading snapshot...")

        if stat(self.file_name).st_size > 0:
            actor = pickle.load(self.file)

            print("Snapshot fetched locally.")
            return (actor, Source.LOCAL)

        print("Snapshot not found locally, trying loading from remote...")
        response = requests.get(self.url)

        if (response.ok):
            actor = pickle.loads(response.content)

            print("Snaphsot loaded remotely.")
            return (actor, Source.REMOTE)

        if not response.ok and response.status_code != 404:
            raise requests.RequestException(
                f"Fail fetching snapshot from object storage\n{response.content}")

        actor = __Actor__()

        print("Snapshot neither found remotely: initialize actor")
        return (actor, Source.NONE)

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
        isolate: bool
            disable actor communicataion capabilities
        persist: bool
            enable snapshot remote persistence 

    Returns
    -------
    out: dict
        the execution results
    '''
    try:
        print(f"\nReceived args: {args}")

        id = args["actor_id"]
        with Repository(id) as repository:
            (actor, source) = repository.load()
            
            __local__: bool
            actor.set_wsk(get_wsk(__local__))

            should_isolate = args["isolate"]
            if should_isolate:
                actor.isolate()

            # Execute code
            msg = args["message"]
            res = actor.receive(msg)

            print(f'\nExecution result: \n {res}\n')

            should_persist = args["persist"]
            repository.dump(actor, should_persist)

        return {
            "result": res,
            "source": source[0],
            "persist": should_persist,
            "isolate": should_isolate
        }

    except Exception:
        return {
            "error": traceback.format_exc()
        }

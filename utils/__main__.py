from __actor__ import __Actor__ as Actor

import traceback
import os
import pickle
import requests
import traceback


class Repository:
    def __init__(self, label: str) -> None:
        self.file_name = label + '.pkl'

    def __enter__(self):
        # Open snapshot file (create if not present) in READ and WRITE mode
        self.file = os.fdopen(
            os.open(self.file_name, os.O_RDWR | os.O_CREAT), 'rb+')
        return self

    def __exit__(self, *args) -> None:
        self.file.close()

    def load(self) -> Actor:
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
        print('Loading local snapshot...')
        if os.stat(self.file_name).st_size > 0:
            print('Snapshot fetched locally')
            return pickle.load(self.file)

        print('Snapshot not found locally, trying loading from remote...')
        response = requests.get(self.url, auth=self.auth)
        if response.status_code == 404:
            print('Snapshot neither found remotely: initialize actor')
            return Actor()

        if not response.ok:
            raise requests.RequestException(
                'Fail fetching snapshot from object storage\n{}'.format(response.content))

        print('Snaphsot loaded remotely')
        return pickle.loads(response.content)

    def dump(self, obj: Actor, remote: bool) -> None:
        '''Dump the actor instance.

        The dump process is executed first locally.
        The produced file is saved to the object storage iff the "remote" parameter is true.

        Raises
        ------
        requests.RequestException
            if the request to upload self.file fails
        '''
        self.file.seek(0)
        pickle.dump(obj, self.file)
        print('Snapshot dumped locally')

        if remote:
            self.file.seek(0)
            response = requests.put(self.url, data=self.file, auth=self.auth)

            if not response.ok:
                raise Exception(
                    'Fail saving snapshot to object storage\n{}'.format(response.content))

            print('Snapshot dumped remotely')


def main(args) -> dict:
    '''Run actor actions in response to messages.

    Attributes
    ----------
    args: dict
        dictionary of parameters to run the right actor actions.

        actor_id: str
            the id of the actor instance
        actor_type: str
            the type of the actor instance
        message: str
            the name of the action to invoke
        offset: int
            the offset of the message, just for logging purposes

    Returns
    -------
    out: dict
        the execution results
    '''
    try:
        label = '{}_{}'.format(args['actor_type'], args['actor_id'])
        with Repository(label) as repository:
            actor: Actor = repository.load()

            # Execute code
            msg = args['message']
            res = actor.receive(msg)

            repository.dump(actor, remote=False)

        return {
            "instance": label,
            "result": res
        }

    except Exception:
        return {
            "error": traceback.format_exc()
        }


res = main({
    'actor_id': 'qwert',
    'actor_type': 'counter',
    'message': 'increment'
})
print(res)

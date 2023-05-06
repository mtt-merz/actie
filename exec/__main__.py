import traceback
from actie import Actor
from repository import Repository

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

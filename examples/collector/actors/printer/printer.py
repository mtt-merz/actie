import json
from lib.actor import Actor


class Printer(Actor):
    def receive(self, msg: str) -> str:
        try:
            data = json.loads(msg)

            title = data['title']
            values = data['data']
        except:
            return ('Wrong message format:' +
                    '\n\treceived {}'.format(msg) +
                    '\n\texpected: { "title": <TITLE>, "data": <DATA> }')

        return f'{title}: {values}'

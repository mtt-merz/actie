import json
from lib.actor import Actor


class Printer(Actor):
    def receive(self, msg: str) -> str:
        try:
            data = json.loads(msg)
            
            title = data['title']
            values = data['data']
        except:
            return 'Wrong message format'
        
        return f'{title}: {values}'
            
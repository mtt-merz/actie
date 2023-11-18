import json
from lib import init_openwhisk


def publish(topic: str, content: str) -> str:
    wsk = init_openwhisk()

    result = wsk.invoke(
        'publish', topic,
        json.dumps({
            "topic": topic,
            "content": content,
        }), result=True
    )

    return json.dumps(result, indent=2)


p = publish("tech", "test")
print(p)

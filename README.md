# Actie Command-line Interface `actie`

Actie Command-line Interface (CLI) is a tool that provides a consistent interface to interact with Actie services.

## Getting started

First of all, clone the project.
Then, move to the project folder and install the required dependencies

```shell
cd actie
pip install -r requirements.txt
```

Now you can install the project itself

```shell
pip install -e .
```

<!-- To actually run actie commands, add the script to your PATH.

```shell
export PATH="$HOME/.local/bin:$PATH"
``` -->

## Create an Actie project

To create a new Actie project, use the Actie CLI as follows

```shell
actie create <PROJECT_NAME>
```

In order to connect to OpenWhisk, you should provide the credentials to access an OpenWhisk running instance. Set them into the `config.json` file in the main folder of the project, toghether with the host of the storage server.

```json
{
    "wsk": {
        "host": <WSK_HOST>,
        "auth": <AUTH>
    },
    "storage": {
        "host": <STORAGE_HOST>
    }
}
```

N.B. The OpenWhisk instance should be aligned with the forked version available [here](https://github.com/mtt-merz/openwhisk).

## Build and deploy an Actie project

To deploy an Actie project, the first step is to build it, using the following command

```shell
actie build
```

It generates the executables of each defined actor. After that, you can simply use the following command to package and register these executable into OpenWhisk.

```shell
actie deploy
```

## Invoke deployed actors

A deployed actor can be invoked by an OpenWhisk instance as follows.

```python
import json
from lib import OpenWhisk

wsk = OpenWhisk.init()
wsk.invoke(
    <ACTOR_FAMILY>, <ACTOR_NAME>,
    json.dumps({
        'action': <STRING>,
        'args': <DICT>
    })
)
```
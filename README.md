# Actie: an Actor Framework for Stateful Serverless Functions

The advent of serverless computing has rapidly transformed the software development landscape by significantly reducing the effort required to build and maintain computing infrastructures. A key player in this transformation is the Function-as-a-Service (FaaS) model, which emerged in the early 2010s and is now supported by many leading cloud providers. FaaS has gained widespread popularity for enabling developers to build scalable, easy-to-deploy functions, billed on a per- invocation basis. This makes it a perfect fit for compute-intensive, highly parallelizable workloads such as Internet of Things and data processing. However, its adoption has been limited by inherent issues such as its low-level abstraction and stateless nature.

To address these challenges we present Actie, a framework designed to simplify the development of stateful and complex serverless applications. Actie’s main contribution lies in its programming abstraction, inspired by the actor model, which enhances FaaS-based applications by enabling a more intuitive design. In addition, Actie introduces a novel state management system, designed to be transparent to developers while improving performance. This mechanism leverages the local memory of serverless functions to create a caching layer, thereby reducing data access and persistence latency. To validate our concept, we implemented Actie on Apache OpenWhisk, a well-known open-source serverless platform. This practical showcase proves the framework’s effectiveness in real-world scenarios. When compared to traditional serverless implementations, Actie demonstrates notable improvements in terms of development complexity and runtime performance, highlighting its potential to contribute to serverless computing advances.

### Credits

Actie is the outcome of the master's thesis research conducted by Matteo Merz at Politecnico di Milano. For further information, please consult the original document, available [here](https://www.politesi.polimi.it/handle/10589/215253).

## Getting started

Actie Command-line Interface (CLI) is a tool that provides a consistent interface to interact with Actie services. Here a quick guide to install and initialize an Actie project.

### Install Actie

First of all, clone the project.
Then, move to the project folder and install the required dependencies

```shell
cd actie
pip install -r requirements.txt
```

Now you can install the framework itself

```shell
pip install -e .
```

<!-- To actually run actie commands, add the script to your PATH.

```shell
export PATH="$HOME/.local/bin:$PATH"
``` -->

### Create an Actie project

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

### Build and deploy an Actie project

To deploy an Actie project, the first step is to build it, using the following command

```shell
actie build
```

It generates the executables of each defined actor. After that, you can simply use the following command to package and register these executable into OpenWhisk.

```shell
actie deploy
```

### Invoke deployed actors

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
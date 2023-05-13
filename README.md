# Actie Command-line Interface `actie`

Actie Command-line Interface (CLI) is a unified tool that provides a consistent interface to interact with Actie services.

## Getting started

First of all, clone the project.
Then, move to the project folder and install the required dependencies

```
cd actie
pip install -r requirements.txt
```

Now you can install the project itself

```
pip install .
```

## Create an Actie project

To create a new Actie project, use the Actie CLI as follows

```
actie create <PROJECT_NAME>
```

In order to connect to OpenWhisk, you should provide the credentials to access an OpenWhisk running instance. Set them into the `config.json` file in the main folder of the project, toghether with the host of the storage server.

```
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

## Run an Actie project

To run an Actie project, move to the project folder and use the Actie CLI as follows

```
actie run
```

If you just need to build the project, you can use the following command

```
actie build
```
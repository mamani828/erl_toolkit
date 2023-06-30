erl-toolkit
===========

Ubuntu CLI for [Existential Robotics Laboratory](http://erl.ucsd.edu/)

# Install

```shell
python3 setup.py --user develop
```

## Docker

- `erl-build-images`: build all images
- `erl-create-container`:
  ```shell
  usage: erl-create-container [-h] --name CONTAINER_NAME --image IMAGE [--gpu] [--command COMMAND] [--user USER] [--overwrite-entrypoint]

  options:
    -h, --help            show this help message and exit
    --name CONTAINER_NAME
    --image IMAGE
    --gpu                 Connect all GPUs to the container
    --command COMMAND
    --user USER           Default: daizhirui
    --overwrite-entrypoint
  ```
- `erl-login-container`:
  ```shell
  usage: erl-login-container [-h] --name CONTAINER_NAME [--user USER] [--shell SHELL]

  options:
    -h, --help            show this help message and exit
    --name CONTAINER_NAME
    --user USER
    --shell SHELL         Default: /usr/bin/zsh
  ```

`erl_toolkit`
===========

CLI for [Existential Robotics Laboratory](http://erl.ucsd.edu/)

# Dependencies

- Docker
- nvidia-docker2 (nvidia-container-toolkit)

```shell
# for ArchLinux
sudo pacman -S docker
paru -S nvidia-docker
```

# Patches

For ArchLinux, you need to apply the following patches. Create two files:
- `/etc/systemd/system/docker.service.d/override.conf`
- `/etc/systemd/system/containerd.service.d/override.conf`

Each file has the following content:
```
[Service]
LimitNOFILE=1048576
```
Then run `sudo systemctl daemon-reload` and reboot your computer.

# Install

```shell
python3 setup.py install --user

# On ArchLinux, to install with system python3, if you get errors, run
python3 setup.py install --user --break-system-packages
```

## Docker

- `erl-build-images`: build all images
- `erl-create-container`:
  ```shell
usage: erl-create-container [-h] --name CONTAINER_NAME --image IMAGE [--gpu] [--dev] [--gui] [--command COMMAND] [--user USER] [--overwrite-entrypoint]

options:
  -h, --help            show this help message and exit
  --name CONTAINER_NAME
  --image IMAGE
  --gpu                 Connect all GPUs to the container
  --dev                 Connect all devices to the container
  --gui                 Connect DISPLAY to the container
  --command COMMAND
  --user USER           Default: $USER
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

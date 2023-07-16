`erl_toolkit`
===========

CLI for [Existential Robotics Laboratory](http://erl.ucsd.edu/)

# Dependencies

- Docker
- nvidia-docker2 (nvidia-container-toolkit)
- pip3

```shell
# for Ubuntu
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
    "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
      sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
    && curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
    && curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt-get update
sudo apt install nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# for ArchLinux
sudo pacman -S docker docker-buildx
paru -S nvidia-docker
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

Test installation:
```shell
sudo docker run --rm --runtime=nvidia --gpus all nvidia/cuda:11.6.2-base-ubuntu20.04 nvidia-smi
```

# Patches

For all Linux distributions, in order to use docker without `sudo`, we need to run:
```shell
sudo usermod -aG docker $USER
newgrp docker  # or reboot your computer
```

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
pip install . --user   # For ArchLinux, add --break-system-packages
```

Export `$HOME/.local/bin` to the `PATH` environment variable:
```shell
export PATH="$HOME/.local/bin:$PATH"
```

# Usage

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
- `erl-clean-docker`: remove stopped containers and redundant image layers.

# FAQ
## Strange cursor position when the last command returns error in zsh
This is already fixed by updating the dockerfiles. But if you do not want to rebuild all the images. You can run the following commands in your current container:
```shell
sudo apt update
sudo apt install locales
sudo sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen
sudo locale-gen
export LANG en_US.UTF-8
export LANGUAGE en_US.UTF-8
export LC_ALL en_US.UTF-8
```

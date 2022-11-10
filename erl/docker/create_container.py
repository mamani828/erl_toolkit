import argparse
import os.path
import socket
from typing import List

import docker
import docker.errors

from erl.docker import CONFIG_DIR
from erl.docker.common import get_container
from erl.log import get_logger

logger = get_logger(__name__)


def create_container(
    name: str,
    image: str,
    command: str = None,
    entrypoint: str = None,
    enable_x11: bool = True,
    auto_remove: bool = False,
    dns: List[str] = None,
    environment: dict = None,
    group_add: list = None,
    mounts: list = None,
    network: str = "host",
    privileged: bool = True,
    restart_policy: dict = None,
    tty: bool = True,
    volumes: list = None,
    user: str = None
):
    client = docker.from_env()
    container = get_container(name)
    if container is not None:
        logger.warning(f"The container {name} already exist.")
        p = input("Do you want to remove the container? [y/N]")
        if p.lower() == "y":
            try:
                if container.status != "exited":
                    logger.warning(f"The container status is {container.status}.")
                    p = input("Do you want to stop it? [y/N]")
                    if p.lower() == "y":
                        container.stop()
                    else:
                        exit(0)
                container.remove()
            except docker.errors.APIError as e:
                print(e)
                exit(1)

    if command is None:
        command = "bash -l"
        auto_remove = False

    if dns is None:
        dns = ["8.8.8.8", "8.8.4.4"]

    if environment is None:
        environment = dict()
    environment["ERL_IN_CONTAINER"] = name
    environment["ERL_DOCKER_IMAGE"] = image

    if restart_policy is None:
        restart_policy = dict(Name="always")

    if volumes is None:
        volumes = set()
    else:
        volumes = set(volumes)
    if enable_x11:
        if not os.path.exists("/tmp/.X11-unix"):
            logger.warn("X11 is unavailable: /tmp/.X11-unix does not exist.")
            exit(1)
        volumes.add("/tmp/.X11-unix:/tmp/.X11-unix")
    for volume in [
        "/var/run/docker.sock",
        "/dev/bus",
        "/dev/block",
        "/dev/char",
        "/dev/serial",
        "/dev/shm",
        os.environ["HOME"],
    ]:
        volume_str = f"{volume}:{volume}:rw"
        if volume_str not in volumes:
            volumes.add(volume_str)
    for volume_str in [
        f"{CONFIG_DIR}:/mnt/docker_login:ro"
    ]:
        if volume_str not in volumes:
            volumes.add(volume_str)
    volumes = list(volumes)

    c = client.containers.run(
        image=image,
        command=command,
        auto_remove=auto_remove,
        detach=True,
        dns=dns,
        entrypoint=entrypoint,
        environment=environment,
        group_add=group_add,
        hostname=f"{socket.gethostname()}-container-{name}",
        mounts=mounts,
        name=name,
        network=network,
        privileged=privileged,
        restart_policy=restart_policy,
        tty=tty,
        user=user,
        volumes=volumes,
        working_dir=os.environ["HOME"],
    )

    for f in [
        "passwd", "group", "shadow"
    ]:
        os.system(f"sudo cp /etc/{f} {os.path.join(CONFIG_DIR, f)}")
        c.exec_run(user="root", cmd=f"cp /mnt/docker_login/{f} /etc/{f}")
        os.system(f"sudo rm {os.path.join(CONFIG_DIR, f)}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", type=str, required=True, metavar="CONTAINER_NAME")
    parser.add_argument("--image", type=str, required=True)
    parser.add_argument("--command", type=str)
    parser.add_argument(
        "--user", type=str, default=f"{os.getuid()}:{os.getgid()}", help=f"Default: {os.getuid()}:{os.getgid()}"
    )
    parser.add_argument("--overwrite-entrypoint", action="store_true")

    args = parser.parse_args()
    entrypoint = None
    if args.overwrite_entrypoint:
        entrypoint = args.command
    create_container(args.name, args.image, args.command, entrypoint=entrypoint)


if __name__ == '__main__':
    main()

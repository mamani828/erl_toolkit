import argparse
import os

import docker

from erl_toolkit.docker import CONTAINER_SHELL
from erl_toolkit.docker.common import get_container
from erl_toolkit.log import get_logger

logger = get_logger(__name__)


def login_container(name: str, user: str, shell: str):
    container = get_container(name)
    if container is None:
        logger.warning(f"No container named {name}. Please create it by erl-new-container at first.")
        exit(1)

    if user == "root":
        home = "/root"
    else:
        home = f"/home/{user}"

    cmd = f"xhost +si:localuser:{user}"
    print(cmd)
    os.system(cmd)
    cmd = (
        f"docker exec --privileged --interactive --tty --env SHELL={shell} --env TERM={os.environ['TERM']} "
        f"--env USER={user} --env=DISPLAY --env=QT_X11_NO_MITSHM=1 --user {user} "
        f"--env HOME={home} {name} {shell} -l"
    )
    print(cmd)
    os.system(cmd)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", type=str, required=True, metavar="CONTAINER_NAME")
    parser.add_argument("--user", type=str, default=os.environ["USER"])
    parser.add_argument("--shell", type=str, default=CONTAINER_SHELL, help=f"Default: {CONTAINER_SHELL}")

    args = parser.parse_args()
    login_container(args.name, args.user, args.shell)


if __name__ == "__main__":
    main()

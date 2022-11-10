import argparse
import os

import docker

from erl.docker import CONTAINER_SHELL
from erl.docker.common import get_container
from erl.log import get_logger

logger = get_logger(__name__)


def login_container(name: str, shell: str):
    container = get_container(name)
    if container is None:
        logger.warning(f"No container named {name}. Please create it by erl-new-container at first.")
        exit(1)

    os.system(f"docker exec --privileged --interactive --tty --env SHELL={shell} --env TERM={os.environ['TERM']} "
              f"--env USER={os.environ['USER']} --env=DISPLAY --env=QT_X11_NO_MITSHM=1 --user {os.environ['USER']} "
              f"--env HOME={os.environ['HOME']} {name} {shell} -l")
    # exit_code, output = container.exec_run(
    #     user=os.environ["USER"],
    #     cmd=f"{shell} -l",
    #     environment=dict(
    #         SHELL=shell,
    #         TERM=os.environ["TERM"],
    #         USER=os.environ["USER"],
    #         DISPLAY=os.environ["DISPLAY"],
    #         QT_X11_NO_MITSHM="1",
    #     ),
    #     tty=True,
    #     privileged=True,
    #     stdin=True
    # )
    # print(exit_code)
    # print(output)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", type=str, required=True, metavar="CONTAINER_NAME")
    parser.add_argument("--shell", type=str, default=CONTAINER_SHELL, help=f"Default: {CONTAINER_SHELL}")

    args = parser.parse_args()
    login_container(args.name, args.shell)


if __name__ == '__main__':
    main()

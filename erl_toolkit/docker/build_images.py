import os
import subprocess
import argparse

import docker

from erl_toolkit.docker import DOCKERFILES


def build_images():
    parser = argparse.ArgumentParser()
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--build-indices", nargs="+", type=int)
    parser.add_argument("--force-rebuild", action="store_true")
    args = parser.parse_args()
    if args.list:
        for i, dockerfile in enumerate(DOCKERFILES):
            print(f"{dockerfile}: {i}")
        return
    if args.build_indices is not None:
        dockerfiles = [DOCKERFILES[i] for i in args.build_indices]
    else:
        dockerfiles = DOCKERFILES
    client = docker.client.from_env()
    for dockerfile in dockerfiles:
        tag = f"erl/{os.path.basename(os.path.dirname(dockerfile))}"
        print("====================================================")
        print(f"Building {tag} ... ", flush=True)
        print("====================================================")
        os.chdir(os.path.dirname(dockerfile))
        if args.force_rebuild:
            subprocess.check_output("bash build.bash --no-cache", shell=True)
        else:
            subprocess.check_output("bash build.bash", shell=True)
        print("DONE", flush=True)


def main():
    build_images()


if __name__ == '__main__':
    main()

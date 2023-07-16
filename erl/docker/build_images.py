import os

import docker

from erl.docker import DOCKERFILES


def build_images():
    client = docker.client.from_env()
    for dockerfile in DOCKERFILES:
        tag = f"erl/{os.path.basename(os.path.dirname(dockerfile))}"
        idx = tag.rfind('-')
        tag = f"{tag[:idx]}:{tag[idx + 1:]}"
        print(f"Building {tag} ... ", end='', flush=True)
        os.chdir(os.path.dirname(dockerfile))
        os.system("bash build.bash")
        # client.images.build(
        #     path=os.path.dirname(dockerfile),
        #     tag=tag,
        #     rm=True,
        #     quiet=False,
        # )
        print("DONE", flush=True)


def main():
    build_images()


if __name__ == '__main__':
    main()

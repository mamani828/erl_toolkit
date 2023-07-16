import os
import subprocess

def main():
    proc = subprocess.run(
        "/usr/bin/docker container ls -a --filter status=exited -q".split(' '),
        capture_output=True,
    )
    containers = [x for x in proc.stdout.decode("utf-8").splitlines() if len(x) > 0]
    if len(containers) > 0:
        p = input("Do you want to remove exited containers? [y/N]")
        if p.lower() == "y":
            os.system(f"docker rm {' '.join(containers)}")

    proc = subprocess.run(
        "/usr/bin/docker images --filter=dangling=true -q".split(' '),
        capture_output=True,
    )
    layers = [x for x in proc.stdout.decode("utf-8").splitlines() if len(x) > 0]
    if len(layers) > 0:
        p = input("Do you want to remove redundant image layers? [y/N]")
        if p.lower() == "y":
            os.system(f"docker rmi {' '.join(layers)}")


if __name__ == "__main__":
    main()

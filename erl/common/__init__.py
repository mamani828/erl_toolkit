import os
import subprocess
from erl.log import get_logger


logger = get_logger(__name__)


def run_command(command: str, get_output: bool = False):
    if get_output:
        p = subprocess.run(executable="/usr/bin/bash", args=f"-c {command}".split(' '), capture_output=True)
        try:
            p.check_returncode()
        except subprocess.CalledProcessError as e:
            logger.warn(f"Failed to run command: {command}")
            print("stdout:", p.stdout.decode("utf-8"), sep="\n")
            print("stderr:", p.stderr.decode("utf-8"), sep="\n")
            exit(p.returncode)
        return dict(
            stdout=p.stdout.decode("utf-8"),
            stderr=p.stderr.decode("utf-8")
        )
    else:
        args = command.split(' ')
        print(args)
        assert len(args) > 0, f"failed to run command: {command}"

        arg0 = args[0]
        args = args[1:]

        if not os.path.exists(arg0):
            arg0 = os.system(f"which {arg0}")

        os.system(f"{arg0} {' '.join(args)}")

import os
import glob
import subprocess
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    if not os.path.exists(args.input):
        print(f"{args.input} does not exist.")
        exit(1)
    if os.path.isfile(args.input):
        files = [args.input]
    else:
        files = glob.glob(f"{args.input}/*")

    if os.path.exists(args.output):
        os.rename(args.output, f"{args.output}.old")

    with open(args.output, "w") as f:
        for file in files:
            if not os.path.isfile(file):
                continue
            cmd = ["/usr/bin/ldd", file]
            result = subprocess.run(cmd, capture_output=True)
            result = result.stdout.decode('utf-8')
            result = result.split('\n')
            result = [x for x in result if "not found" in x]
            if len(result) == 0:
                continue
            result = "\n".join(result)
            print(file)
            print(result)

            f.write(file + '\n')
            f.write(result + '\n')


if __name__ == "__main__":
    main()

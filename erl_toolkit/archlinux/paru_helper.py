import subprocess
import time
import os
from argparse import ArgumentParser
from argparse import _HelpAction as HelpAction
from argparse import _SubParsersAction as SubParsersAction


def check_paru():
    p = subprocess.run(
        ["paru", "-V"],
        capture_output=True,
        text=True,
    )
    if p.returncode != 0:
        print(p.stderr)
        print("try to install paru ...")
        os.system("git clone https://aur.archlinux.org/paru.git")
        cwd = os.getcwd()
        os.chdir("paru")
        os.system("makepkg -si --noconfirm -c")
        os.chdir(cwd)
        os.system("rm -rf paru")
        check_paru()
    else:
        print(p.stdout)


def get_installed_packages():
    return subprocess.run(
        ["paru", "-Qq"],
        capture_output=True,
        text=True,
    ).stdout.splitlines()


def get_package_info(package_name):
    def clean_names(names):
        cleaned_names = []
        for x in names:
            x = x.strip()
            if len(x) == 0:
                continue
            if x == "None":
                continue
            if "==" in x:
                x = x.replace("==", "-")
            if "=" in x:
                x = x.replace("=", "-")
            if ">=" in x:
                x = x.split(">=")[0]
            if ">" in x:
                x = x.split(">")[0]
            if "<=" in x:
                x = x.split("<=")[0]
            if "<" in x:
                x = x.split("<")[0]
            cleaned_names.append(x)
        return cleaned_names

    p = subprocess.run(
        ["paru", "-Si", package_name],
        capture_output=True,
        text=True,
    )
    if p.returncode != 0:
        print(p.stderr)
        raise RuntimeError("paru returned non-zero exit code")
    results = p.stdout.splitlines()

    results = [line.split(": ") for line in results if ": " in line]
    results = {items[0].strip(): items[1].strip() for items in results if len(items) == 2}
    results["Depends On"] = clean_names(results["Depends On"].split(" "))
    if len(results["Depends On"]) == 0:
        del results["Depends On"]
    # results["Optional Deps"] = [x for x in [x.strip() for x in results["Optional Deps"].split(" ")] if len(x) > 0]
    # if results["Optional Deps"][0] == "None":
    #     del results["Optional Deps"]
    if results["Repository"] == "aur":
        results["Make Deps"] = clean_names(results["Make Deps"].split(" "))
        if len(results["Make Deps"]) == 0:
            del results["Make Deps"]
        results["Check Deps"] = clean_names(results["Check Deps"].split(" "))
        if len(results["Check Deps"]) == 0:
            del results["Check Deps"]
    return results


def dump_required_dependencies(
    package_name, sink_package_names: set, is_sink_packge=None, ignore_packages=None
) -> dict:
    if not isinstance(sink_package_names, set):
        raise TypeError("sink_package_names must be a set")
    # if len(sink_package_names) == 0:
    #     sink_package_names = set(["sh", "cargo"])
    required_dependencies = dict()
    if ignore_packages is None:
        ignore_packages = set()
    try:
        package_info = get_package_info(package_name)
    except RuntimeError:
        sink_package_names.add(package_name)
        return required_dependencies

    if package_info["Repository"] != "aur":
        return required_dependencies  # stop recursion when we hit a non-aur package

    required_dependencies[package_name] = list(
        set(package_info.get("Depends On", []) + package_info.get("Make Deps", []) + package_info.get("Check Deps", []))
    )
    ignore_packages.add(package_name)
    for dependency in required_dependencies[package_name]:
        if is_sink_packge is not None and is_sink_packge(dependency):
            sink_package_names.add(dependency)
        if dependency in ignore_packages:  # prevent infinite recursion
            continue
        if dependency not in sink_package_names:
            required_dependencies.update(
                dump_required_dependencies(dependency, sink_package_names, is_sink_packge, ignore_packages)
            )

    return required_dependencies


def test():
    check_paru()

    tic = time.perf_counter()
    sink_packages = set()
    dependencies = dump_required_dependencies(
        "ros-noetic-desktop-full",
        sink_packages,
        is_sink_packge=lambda x: not x.startswith("ros-noetic-") and x not in ["gazebo"],
    )
    toc = time.perf_counter()
    print(f"dump_required_dependencies() took {toc - tic:0.4f} seconds")

    sink_packages = list(sink_packages)
    sink_packages.sort()
    print("sink_packages:")
    print(sink_packages)

    print("dependencies:")
    print(dependencies)


def main():

    class CompleteHelpAction(HelpAction):
        def __call__(self, parser, namespace, values, option_string=None):
            parser.print_help()
            subparsers_actions = [
                action
                for action in parser._actions
                if isinstance(action, SubParsersAction)
            ]
            print()
            for subparsers_action in subparsers_actions:
                for choice, subparser in subparsers_action.choices.items():
                    print(f"Command: {choice}")
                    print(subparser.format_help())
                    print()
            parser.exit()

    parser = ArgumentParser(description="paru helper", add_help=False)
    parser.add_argument("--help", "-h", action=CompleteHelpAction, help="show this help message and exit")
    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
        metavar="COMMAND",
        help="Options: dump-required-dependencies"
    )
    parser_dump_required_dependencies = subparsers.add_parser("dump-required-dependencies")
    parser_dump_required_dependencies.add_argument("package_name", type=str)
    parser_dump_required_dependencies.add_argument(
        "--sink-packages",
        nargs="+",
        default=[],
        metavar="PACKAGES",
        help="Initial sink packages, dependency search will stop when these packages are hit.",
    )
    parser_dump_required_dependencies.add_argument(
        "--is-sink-package",
        type=str,
        metavar="LAMBDA_EXPRESSION",
        help="lambda expression to determine whether a package is a sink package.",
    )
    parser_dump_required_dependencies.add_argument(
        "--ignore-packages",
        nargs="+",
        default=[],
        metavar="PACKAGES",
        help="Ignore these packages. They will not be in the result.",
    )
    parser_dump_required_dependencies.add_argument(
        "--output-format",
        type=str,
        choices=["raw", "yaml"],
        default="raw",
        help="Output format.",
    )
    args = parser.parse_args()

    if args.command == "dump-required-dependencies":
        sink_packages = set(args.sink_packages)
        ignore_packages = set(args.ignore_packages)
        if args.is_sink_package is not None:
            is_sink_package = eval(args.is_sink_package)
        else:
            is_sink_package = None
        dependencies = dump_required_dependencies(args.package_name, sink_packages, is_sink_package, ignore_packages)
        if args.output_format == "raw":
            print("sink_packages:")
            print(sorted(list(sink_packages)))
            print("dependencies:")
            print(dependencies)
        elif args.output_format == "yaml":
            import yaml

            result = dict(sink_packages=sorted(list(sink_packages)), dependencies=dependencies)
            print(yaml.dump(result))


if __name__ == "__main__":
    main()

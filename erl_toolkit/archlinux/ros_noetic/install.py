import os
import sys
from tqdm import tqdm
from argparse import ArgumentParser


def main():
    mkl_lib_path = "/opt/intel/oneapi/mkl/latest/lib/intel64"
    ld_library_path = os.environ.get("LD_LIBRARY_PATH", "")
    if mkl_lib_path not in ld_library_path:
        if len(ld_library_path) == 0:
            os.environ["LD_LIBRARY_PATH"] = mkl_lib_path
        else:
            os.environ["LD_LIBRARY_PATH"] = f"{mkl_lib_path}:{ld_library_path}"
    from erl_toolkit.archlinux.ros_noetic.dependencies import dependencies
    from erl_toolkit.archlinux.ros_noetic.sink_packages import sink_packages
    sink_packages = list(set(sink_packages))
    sink_packages.sort()

    alternative_selections = {
        "pkg-config": "pkgconf",
        "opencv": "opencv-cuda",
        "python-sip4": "sip4",
        "python-pyqt5": "python-pyqt5-sip4",
        "python-numpy": "python-numpy-mkl",
        "ogre": "ogre-1.9",
        "python-sip": "sip4",
        "ruby-ronn": "ruby-ronn-ng",
        "tbb": "onetbb",
        "gmock": "gtest",
        "libltdl": "libtool",
        "python-empy": "python-empy3",
    }

    use_git_packages = [
        "eigen",
        "gazebo",
        "pcl",
        "fcl",
    ]

    # place replacement urls here if the package is not available in AUR or the AUR package is broken
    aur_package_urls = {
        # "sip4": "https://github.com/daizhirui/sip4.git",
        "ros-noetic-amcl": "https://github.com/daizhirui/ros-noetic-amcl.git",
        "ros-noetic-base-local-planner": "https://github.com/daizhirui/ros-noetic-base-local-planner.git",
        "ros-noetic-camera-calibration": "https://github.com/daizhirui/ros-noetic-camera-calibration.git",
        "ros-noetic-camera-calibration-parser": "https://github.com/daizhirui/ros-noetic-camera-calibration-parser.git",
        "ros-noetic-camera-info-manager": "https://github.com/daizhirui/ros-noetic-camera-info-manager.git",
        "ros-noetic-catkin": "https://github.com/daizhirui/ros-noetic-catkin.git",
        "ros-noetic-costmap-2d": "https://github.com/daizhirui/ros-noetic-costmap-2d.git",
        "ros-noetic-compressed-depth-image-transport": "https://github.com/daizhirui/ros-noetic-compressed-depth-image-transport.git",
        "ros-noetic-compressed-image-transport": "https://github.com/daizhirui/ros-noetic-compressed-image-transport.git",
        "ros-noetic-controller-interface": "https://github.com/daizhirui/ros-noetic-controller-interface.git",
        "ros-noetic-controller-manager": "https://github.com/daizhirui/ros-noetic-controller-manager.git",
        "ros-noetic-controller-manager-msgs": "https://github.com/daizhirui/ros-noetic-controller-manager-msgs.git",
        "ros-noetic-cpp-common": "https://github.com/daizhirui/ros-noetic-cpp-common.git",
        "ros-noetic-diff-drive-controller": "https://github.com/daizhirui/ros-noetic-diff-drive-controller.git",
        "ros-noetic-dynamic-reconfigure": "https://github.com/daizhirui/ros-noetic-dynamic-reconfigure.git",
        "ros-noetic-eigen-conversions": "https://github.com/ros-noetic-arch/ros-noetic-eigen-conversions.git",
        "ros-noetic-rqt-action": "https://github.com/daizhirui/ros-noetic-rqt-action.git",
        "ros-noetic-rqt-bag": "https://github.com/daizhirui/ros-noetic-rqt-bag.git",
        "ros-noetic-rqt-bag-plugins": "https://github.com/daizhirui/ros-noetic-rqt-bag-plugins.git",
        "ros-noetic-rqt-console": "https://github.com/daizhirui/ros-noetic-rqt-console.git",
        "ros-noetic-rqt-dep": "https://github.com/daizhirui/ros-noetic-rqt-dep.git",
        "ros-noetic-rqt-graph": "https://github.com/daizhirui/ros-noetic-rqt-graph.git",
        "ros-noetic-rqt-image-view": "https://github.com/daizhirui/ros-noetic-rqt-image-view.git",
        "ros-noetic-rqt-launch": "https://github.com/daizhirui/ros-noetic-rqt-launch.git",
        "ros-noetic-rqt-logger-level": "https://github.com/daizhirui/ros-noetic-rqt-logger-level.git",
        "ros-noetic-rqt-moveit": "https://github.com/daizhirui/ros-noetic-rqt-moveit.git",
        "ros-noetic-rqt-msg": "https://github.com/daizhirui/ros-noetic-rqt-msg.git",
        "ros-noetic-rqt-nav-view": "https://github.com/daizhirui/ros-noetic-rqt-nav-view.git",
        "ros-noetic-rqt-pose-view": "https://github.com/daizhirui/ros-noetic-rqt-pose-view.git",
        "ros-noetic-rqt-publisher": "https://github.com/daizhirui/ros-noetic-rqt-publisher.git",
        "ros-noetic-rqt-py-console": "https://github.com/daizhirui/ros-noetic-rqt-py-console.git",
        "ros-noetic-forward-command-controller": "https://github.com/daizhirui/ros-noetic-forward-command-controller.git",
        "ros-noetic-genpy": "https://github.com/daizhirui/ros-noetic-genpy.git",
        "ros-noetic-hardware-interface": "https://github.com/daizhirui/ros-noetic-hardware-interface.git",
        "ros-noetic-image-pipeline": "https://github.com/daizhirui/ros-noetic-image-pipeline.git",
        "ros-noetic-image-proc": "https://github.com/daizhirui/ros-noetic-image-proc.git",
        "ros-noetic-image-publisher": "https://github.com/daizhirui/ros-noetic-image-publisher.git",
        "ros-noetic-image-rotate": "https://github.com/daizhirui/ros-noetic-image-rotate.git",
        "ros-noetic-image-transport": "https://github.com/daizhirui/ros-noetic-image-transport.git",
        "ros-noetic-image-transport-plugins": "https://github.com/daizhirui/ros-noetic-image-transport-plugins.git",
        "ros-noetic-image-view": "https://github.com/daizhirui/ros-noetic-image-view.git",
        "ros-noetic-rosconsole": "https://github.com/daizhirui/ros-noetic-rosconsole.git",
        "ros-noetic-robot-state-publisher": "https://github.com/daizhirui/ros-noetic-robot-state-publisher.git",
        "ros-noetic-depth-image-proc": "https://github.com/daizhirui/ros-noetic-depth-image-proc.git",
        "ros-noetic-laser-assembler": "https://github.com/daizhirui/ros-noetic-laser-assembler.git",
        "ros-noetic-laser-filters": "https://github.com/daizhirui/ros-noetic-laser-filters.git",
        "ros-noetic-robot-localization": "https://github.com/daizhirui/ros-noetic-robot-localization.git",
        "ros-noetic-joint-state-controller": "https://github.com/daizhirui/ros-noetic-joint-state-controller.git",
        "ros-noetic-joint-limits-interface": "https://github.com/daizhirui/ros-noetic-joint-limits-interface.git",
        "ros-noetic-roscpp-core": "https://github.com/daizhirui/ros-noetic-roscpp-core.git",
        "ros-noetic-rostime": "https://github.com/daizhirui/ros-noetic-rostime.git",
        "ros-noetic-roscpp-traits": "https://github.com/daizhirui/ros-noetic-roscpp-traits.git",
        "ros-noetic-joint-state-publisher-gui": "https://github.com/daizhirui/ros-noetic-joint-state-publisher-gui.git",
        "ros-noetic-roscpp": "https://github.com/daizhirui/ros-noetic-roscpp.git",
        "ros-noetic-roscpp-serialization": "https://github.com/daizhirui/ros-noetic-roscpp-serialization.git",
        "ros-noetic-roscpp-tutorials": "https://github.com/daizhirui/ros-noetic-roscpp-tutorials.git",
        "ros-noetic-roslaunch": "https://github.com/daizhirui/ros-noetic-roslaunch.git",
        "ros-noetic-roslib": "https://github.com/daizhirui/ros-noetic-roslib.git",
        "ros-noetic-rosgraph": "https://github.com/daizhirui/ros-noetic-rosgraph.git",
        "ros-noetic-kdl-conversions": "https://github.com/daizhirui/ros-noetic-kdl-conversions.git",
        "ros-noetic-map-server": "https://github.com/daizhirui/ros-noetic-map-server.git",
        "ros-noetic-move-base": "https://github.com/daizhirui/ros-noetic-move-base.git",
        "ros-noetic-nav-core": "https://github.com/daizhirui/ros-noetic-nav-core.git",
        "ros-noetic-navfn": "https://github.com/daizhirui/ros-noetic-navfn.git",
        "ros-noetic-nodelet": "https://github.com/daizhirui/ros-noetic-nodelet.git",
        "ros-noetic-nodelet-core": "https://github.com/daizhirui/ros-noetic-nodelet-core.git",
        "ros-noetic-nodelet-topic-tools": "https://github.com/daizhirui/ros-noetic-nodelet-topic-tools.git",
        "ros-noetic-pcl-conversions": "https://github.com/daizhirui/ros-noetic-pcl-conversions.git",
        "ros-noetic-pcl-msgs": "https://github.com/daizhirui/ros-noetic-pcl-msgs.git",
        "orocos-kdl-python": "https://github.com/daizhirui/arch-orocos-kdl-python.git",
    }

    parser = ArgumentParser(description="Install/fix ros-noetic-desktop-full and its dependencies.")
    parser.add_argument(
        "--start-from",
        nargs="+",
        default=[],
        metavar="PACKAGES",
        help="Start the installation from these packages, and install other packages requiring them.",
    )
    args = parser.parse_args()
    args_start_from = set(args.start_from)

    # compute the order of installation
    dependency_graph = {k: set(v) for k, v in dependencies.items()}

    if len(args_start_from) > 0:
        # compute the reverse dependency graph
        rdependency_graph = dict()
        for package_name, package_dependencies in dependencies.items():
            for dependency in package_dependencies:
                if dependency not in rdependency_graph:
                    rdependency_graph[dependency] = set()
                rdependency_graph[dependency].add(package_name)

        sink_packages = list(set(args.start_from))

        tiny_dependency_graph = dict()
        involved_packages = set(sink_packages)
        while len(involved_packages) > 0:
            next_involved_packages = set()
            for package in involved_packages:
                if package not in rdependency_graph:  # top-level package
                    continue
                for affected_pkg in rdependency_graph[package]:  # affected packages
                    if affected_pkg not in tiny_dependency_graph:
                        tiny_dependency_graph[affected_pkg] = set()
                        next_involved_packages.add(affected_pkg)
                    tiny_dependency_graph[affected_pkg].add(package)
            involved_packages = next_involved_packages

        order = [sink_packages]
        while len(tiny_dependency_graph) > 0:
            cur_order = order[-1]
            next_order = set()
            for package in cur_order:
                for required_by in tiny_dependency_graph.keys():
                    tiny_dependency_graph[required_by].discard(package)  # remove the dependency
                    if len(tiny_dependency_graph[required_by]) == 0:  # no more dependencies, can be installed
                        next_order.add(required_by)
            for package in next_order:
                del tiny_dependency_graph[package]
            if len(next_order) == 0:
                if len(tiny_dependency_graph) > 0:
                    print("Circular/Incomplete dependency detected!")
                    sys.exit(1)
            order.append(list(next_order))
    else:
        order = [sink_packages]
        while len(dependency_graph) > 0:
            cur_order = order[-1]
            next_order = set()
            for package in cur_order:
                for required_by in dependency_graph.keys():
                    dependency_graph[required_by].discard(package)  # remove the dependency
                    if len(dependency_graph[required_by]) == 0:  # no more dependencies, can be installed
                        next_order.add(required_by)
            for package in next_order:
                del dependency_graph[package]
            if len(next_order) == 0:
                if len(dependency_graph) > 0:
                    print(dependency_graph)
                    print("Circular/Incomplete dependency detected!")
                    sys.exit(1)
                break
            order.append(list(next_order))

    answer = input("Do you want to start installing? [y/N] ")
    if answer.lower() != "y":
        sys.exit(0)


    def exit_on_failure(cmd):
        if os.system(cmd) != 0:
            sys.exit(1)


    # install packages
    paru_dir = os.path.join(os.environ["HOME"], ".cache", "paru", "clone")
    os.chdir(paru_dir)
    installed_packages = set()
    if os.path.exists("progress.txt"):
        with open("progress.txt", "r") as f:
            installed_packages = set([line.strip() for line in f.readlines()])
    with open("progress.txt", "a+") as progress:
        pbar = tqdm(total=sum([len(packages) for packages in order]), ncols=80)
        for packages in order:
            for package in packages:
                if package in alternative_selections:
                    package = alternative_selections[package]
                if package in use_git_packages:
                    package = f"{package}-git"
                if package in installed_packages:
                    pbar.update()
                    continue
                if not os.path.exists(package):
                    if package in aur_package_urls:
                        os.system(f"git clone {aur_package_urls[package]} {package}")
                    else:
                        # if os.system(f"paru -G {package}") != 0:
                        if os.system(f"pacman -Si {package}") == 0:  # exist package by pacman
                            os.system(f"paru -S {package} --noconfirm")
                            installed_packages.add(package)
                            progress.write(f"{package}\n")
                            progress.flush()
                            pbar.update()
                            continue
                        else:
                            os.system(f"paru -G {package}")
                else:
                    if package in aur_package_urls:
                        os.chdir(package)
                        os.system(f"git remote set-url origin {aur_package_urls[package]}")
                        os.chdir(paru_dir)
                os.chdir(package)
                if package in aur_package_urls:
                    os.system(f"git remote set-url origin {aur_package_urls[package]}")
                os.system("git reset --hard")
                os.system("git pull --rebase")  # update the package
                if os.system("makepkg -si --noconfirm -c") != 0:  # dependencies are incomplete?
                    with open("../ros-noetic-install.log", "a") as log_file:
                        log_file.write(f"makepkg failed for {package}, some dependencies may not be recorded\n")
                    exit_on_failure(f"paru -S {package} --noconfirm")
                # exit_on_failure("rm -rf pkg src *.pkg.tar.zst")
                exit_on_failure("rm -rf pkg src")
                os.chdir(paru_dir)
                installed_packages.add(package)
                progress.write(f"{package}\n")
                progress.flush()
                pbar.update()
    os.remove("progress.txt")


if __name__ == "__main__":
    main()

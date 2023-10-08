import os.path

from setuptools import setup, find_packages


src_dir = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(src_dir, "requirements.txt"), "r") as file:
    requires = file.readlines()
    requires = [r.strip() for r in requires]

os.chdir(src_dir)

pkg_name = "erl_toolkit"
setup(
    name=pkg_name,
    version="0.1.0",
    install_requires=requires,
    packages=find_packages(),
    package_dir={pkg_name: pkg_name},
    include_package_data=True,
    entry_points=dict(
        console_scripts=[
            f"erl-docker-create-container={pkg_name}.docker.create_container:main",
            f"erl-docker-login-container={pkg_name}.docker.login_container:main",
            f"erl-docker-build-images={pkg_name}.docker.build_images:main",
            f"erl-docker-clean-docker={pkg_name}.docker.clean_docker:main",
            f"erl-archlinux-ros-noetic-install={pkg_name}.archlinux.ros_noetic.install:main",
            f"erl-archlinux-paru-helper={pkg_name}.archlinux.paru_helper:main",
        ]
    )
)

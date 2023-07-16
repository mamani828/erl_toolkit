import os.path

from setuptools import setup, find_packages


src_dir = os.path.dirname(os.path.realpath(__file__))


with open(os.path.join(src_dir, "requirements.txt"), "r") as file:
    requires = file.readlines()
    requires = [r.strip() for r in requires]

os.chdir(src_dir)

pkg_name = "erl"
setup(
    name="erl",
    version="0.1.0",
    install_requires=requires,
    packages=find_packages(src_dir),
    package_dir={"erl": os.path.join(src_dir, "erl")},
    entry_points=dict(
        console_scripts=[
            "erl-create-container=erl.docker.create_container:main",
            "erl-login-container=erl.docker.login_container:main",
            "erl-build-images=erl.docker.build_images:main",
            "erl-clean-docker=erl.docker.clean_docker:main"
        ]
    )
)

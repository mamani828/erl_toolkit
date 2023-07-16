import glob
import os

CONFIG_DIR = os.path.join(os.environ["HOME"], ".config", "erl", "docker")
if not os.path.exists(CONFIG_DIR):
    os.makedirs(CONFIG_DIR)
CONTAINER_SHELL = os.environ["SHELL"]

DOCKERFILES_DIR = os.path.dirname(os.path.abspath(__file__))
DOCKERFILES_DIR = os.path.join(DOCKERFILES_DIR, "dockerfiles")
DOCKERFILES = [
    os.path.join(DOCKERFILES_DIR, "ubuntu-18.04/Dockerfile"),
    os.path.join(DOCKERFILES_DIR, "ubuntu-desktop-18.04/Dockerfile"),
    os.path.join(DOCKERFILES_DIR, "ubuntu-desktop-20.04/Dockerfile"),
    os.path.join(DOCKERFILES_DIR, "ubuntu-desktop-22.04/Dockerfile"),
    os.path.join(DOCKERFILES_DIR, "ros-noetic/Dockerfile"),
]

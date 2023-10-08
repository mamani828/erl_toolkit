#! /usr/bin/bash
docker build --rm -t erl/ros-noetic .
docker build --rm -t erl/ros-noetic:cpu --build-arg BASE_IMAGE=erl/ubuntu-desktop:20.04 .

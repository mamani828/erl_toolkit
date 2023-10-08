ARG CUDA_VERSION="12.1.1-cudnn8-devel-ubuntu20.04"
ARG BASE_IMAGE=erl/ubuntu-desktop:${CUDA_VERSION}
FROM ${BASE_IMAGE}

RUN sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
RUN curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -
RUN DEBIAN_FRONTEND=noninteractive apt update -y
RUN DEBIAN_FRONTEND=noninteractive apt install -y \
    ros-noetic-desktop-full \
    python3-rosdep \
    python3-rosinstall \
    python3-rosinstall-generator \
    python3-wstool \
    python3-catkin-tools
RUN sudo rosdep init && sudo rosdep fix-permissions
RUN apt-get clean  && rm -rf /var/lib/apt/lists/*

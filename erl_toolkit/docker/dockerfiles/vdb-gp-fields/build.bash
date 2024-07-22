#!/usr/bin/env bash

set -e
set -x
CUDA_VERSION="12.3.2-cudnn9-devel-ubuntu20.04"
docker build --rm -t erl/vdb-gp-fields:latest --build-arg BASE_IMAGE=erl/ros-noetic:${CUDA_VERSION} $@ .

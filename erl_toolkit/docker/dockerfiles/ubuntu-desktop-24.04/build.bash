#! /usr/bin/bash
set -e
set -x

docker build --rm \
    --build-arg BASE_IMAGE=ubuntu:22.04 \
    -t erl/ubuntu-desktop:22.04 $@ .

CUDA_VERSION="12.1.1-cudnn8-devel-ubuntu22.04"
docker build --rm \
    --build-arg BASE_IMAGE=nvidia/cuda:${CUDA_VERSION} \
    -t erl/ubuntu-desktop:${CUDA_VERSION} $@ .

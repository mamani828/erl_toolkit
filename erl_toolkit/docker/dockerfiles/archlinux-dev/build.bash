#! /usr/bin/bash
set -e
set -x

docker build --rm \
    -t erl/archlinux:base-devel $@ .

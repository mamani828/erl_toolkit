#! /usr/bin/bash
set -e
set -x

docker build --rm -t erl/ubuntu:18.04 $@ .

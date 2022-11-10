FROM ubuntu:18.04

RUN DEBIAN_FRONTEND=noninteractive apt update -y
RUN DEBIAN_FRONTEND=noninteractive apt install -y \
    ubuntu-desktop zsh ca-certificates curl

# Kubernetes
RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
RUN install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# clean
RUN apt-get clean  && rm -rf /var/lib/apt/lists/*

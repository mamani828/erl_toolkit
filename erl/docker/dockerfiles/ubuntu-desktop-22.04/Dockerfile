ARG BASE_IMAGE=ubuntu:22.04
FROM ${BASE_IMAGE}

COPY ./sources.list /etc/apt
RUN DEBIAN_FRONTEND=noninteractive apt update -y

RUN DEBIAN_FRONTEND=noninteractive apt install -y \
    software-properties-common lsb-release wget vim locales

# cmake
RUN wget -O - https://apt.kitware.com/keys/kitware-archive-latest.asc 2>/dev/null | gpg --dearmor - | tee /etc/apt/trusted.gpg.d/kitware.gpg >/dev/null
RUN apt-add-repository "deb https://apt.kitware.com/ubuntu/ $(lsb_release -cs) main"
RUN DEBIAN_FRONTEND=noninteractive apt update -y
RUN DEBIAN_FRONTEND=noninteractive apt install kitware-archive-keyring
RUN DEBIAN_FRONTEND=noninteractive apt install -y \
    cmake build-essential

RUN DEBIAN_FRONTEND=noninteractive apt install -y \
    sudo zsh ca-certificates curl iproute2

RUN DEBIAN_FRONTEND=noninteractive apt install -y ubuntu-desktop

# Kubernetes
RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
RUN install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# set locale
RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8
ENV LC_ALL en_US.UTF-8

# clean
RUN apt-get clean  && rm -rf /var/lib/apt/lists/*

ENV TZ="America/Los_Angeles"
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

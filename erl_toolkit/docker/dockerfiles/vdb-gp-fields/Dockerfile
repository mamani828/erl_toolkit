FROM erl/ros-noetic:12.3.2-cudnn9-devel-ubuntu20.04

ENV DEBIAN_FRONTEND noninteractive
WORKDIR /root

RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.1.2/zsh-in-docker.sh)" -- \
    -t robbyrussell \
    -p git \
    -p ssh-agent \
    -p https://github.com/agkozak/zsh-z \
    -p https://github.com/zsh-users/zsh-autosuggestions \
    -p https://github.com/zsh-users/zsh-completions \
    -p https://github.com/zsh-users/zsh-syntax-highlighting

# Install extra ROS packages and OpenVDB dependencies
RUN apt update -y && apt install -y \
    ros-noetic-tf2-sensor-msgs \
    libblosc-dev \
    libboost-iostreams-dev \
    libboost-system-dev \
    libboost-system-dev \
    libeigen3-dev \
    libatlas-base-dev

# Install OpenVDB from source
RUN git clone --depth 1 https://github.com/nachovizzo/openvdb.git -b nacho/vdbfusion \
    && cd openvdb \
    && mkdir build && cd build \
    && cmake  -DCMAKE_POSITION_INDEPENDENT_CODE=ON -DUSE_ZLIB=OFF .. \
    && make -j$(nproc) all install \
    && cd /root \
    && rm -rf /openvdb

# Install Open3D dependencies
RUN git clone --depth 1 --branch v0.16.0 https://github.com/isl-org/Open3D.git && cd Open3D \
    && util/install_deps_ubuntu.sh assume-yes && mkdir build && cd build && cmake .. \
    && make -j$(nproc) \
    && make -j$(nproc) all install \
    && cd /root \
    && rm -rf /Open3D

# Install glog
RUN git clone https://github.com/google/glog.git && cd glog \
    && git fetch --all --tags \
    && git checkout tags/v0.4.0 -b v0.4.0 \
    && mkdir build && cd build \
    && cmake .. \
    && make -j$(nproc) \
    && make install \
    && cd /root \
    && rm -rf /glog

# Install gflags
RUN git clone https://github.com/gflags/gflags.git && cd gflags \
    && mkdir build && cd build \
    && cmake .. -DBUILD_SHARED_LIBS=ON \
    && make -j$(nproc) \
    && make install \
    && cd /root \
    && rm -rf /gflags

# Install Ceres
RUN git clone https://github.com/ceres-solver/ceres-solver && cd ceres-solver \
    && git fetch --all --tags \
    && git checkout tags/2.2.0 -b 2.2.0 \
    && mkdir build && cd build \
    && cmake .. \
    && make -j$(nproc) \
    && make install \
    && cd /root \
    && rm -rf /ceres-solver

# Install fmt
RUN git clone https://github.com/fmtlib/fmt.git && cd fmt \
    && mkdir build && cd build \
    && cmake .. \
    && make -j$(nproc) \
    && make install \
    && cd /root \
    && rm -rf /fmt

ENV DEBIAN_FRONTEND=

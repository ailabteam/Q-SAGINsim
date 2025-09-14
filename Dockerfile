# Start from Ubuntu 22.04
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

# Install all system dependencies
RUN apt-get update && apt-get install -y \
    wget bzip2 git cmake g++ python3.10 python3-pip \
    libzmq3-dev libprotobuf-dev protobuf-compiler pkg-config nano

# Set python3.10 as default
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1

# Create a working directory
WORKDIR /workspace

# Download and extract ns-3
RUN wget https://www.nsnam.org/releases/ns-allinone-3.40.tar.bz2 && \
    tar xf ns-allinone-3.40.tar.bz2

# Clone ns3-gym
RUN git clone https://github.com/tkn-tub/ns3-gym.git /workspace/ns-allinone-3.40/ns-3.40/contrib/opengym

# Configure and build ns-3
RUN cd /workspace/ns-allinone-3.40/ns-3.40 && \
    ./ns3 configure --enable-examples && \
    ./ns3 build

# === FINAL FIX: Install ALL Python packages in one go ===
RUN pip3 install \
    gymnasium \
    sequence \
    /workspace/ns-allinone-3.40/ns-3.40/contrib/opengym/model/ns3gym

# Copy our framework
COPY . /app
WORKDIR /app

CMD ["bash"]

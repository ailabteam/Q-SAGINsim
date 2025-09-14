# Giai đoạn 1: Base Image - Cài đặt tất cả các gói phụ thuộc
# Sử dụng Ubuntu 22.04 làm nền tảng
FROM ubuntu:22.04 AS base

# Tránh các câu hỏi tương tác trong quá trình cài đặt
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

# Cài đặt tất cả các gói phụ thuộc hệ thống bằng apt-get
# Đây là bước quan trọng để đảm bảo tính tương thích
RUN apt-get update && apt-get install -y \
    wget \
    bzip2 \
    git \
    cmake \
    g++ \
    pkg-config \
    python3.10 \
    python3-pip \
    libzmq3-dev \
    libprotobuf-dev \
    protobuf-compiler \
    nano \
    && rm -rf /var/lib/apt/lists/*

# Thiết lập python3.10 là python mặc định
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1

# Cài đặt các thư viện Python cần thiết cho ns3-gym
RUN pip3 install --no-cache-dir protobuf==3.20.3 grpcio-tools==1.47.0 gymnasium

# Giai đoạn 2: Build - Biên dịch ns-3 và ns3-gym
FROM base AS builder

# Tạo thư mục làm việc
WORKDIR /workspace

# Tải và giải nén ns-allinone-3.40
RUN wget https://www.nsnam.org/releases/ns-allinone-3.40.tar.bz2 && \
    tar xf ns-allinone-3.40.tar.bz2

# Clone ns3-gym vào đúng vị trí
RUN git clone https://github.com/tkn-tub/ns3-gym.git /workspace/ns-allinone-3.40/ns-3.40/contrib/opengym

# Cấu hình và build ns-3. Bước này sẽ mất nhiều thời gian nhất.
RUN cd /workspace/ns-allinone-3.40/ns-3.40 && \
    ./ns3 configure --enable-examples && \
    ./ns3 build

# Giai đoạn 3: Final Image - Tạo image cuối cùng gọn nhẹ
FROM base AS final

# Tạo thư mục và sao chép các thành phần đã được build từ giai đoạn 'builder'
COPY --from=builder /workspace/ns-allinone-3.40 /workspace/ns-allinone-3.40

# Cài đặt phần Python của ns3-gym
RUN pip3 install /workspace/ns-allinone-3.40/ns-3.40/contrib/opengym/model/ns3gym

# Sao chép framework Q-SAGINsim của bạn vào container
COPY . /app

# Thiết lập thư mục làm việc mặc định
WORKDIR /app

# Lệnh mặc định khi chạy container
CMD ["bash"]

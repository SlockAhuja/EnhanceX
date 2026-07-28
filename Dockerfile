# Multi-stage production container for EnhanceX with CUDA 12.1 acceleration
FROM nvidia/cuda:12.1.0-devel-ubuntu22.04 AS builder

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.10 \
    python3.10-dev \
    python3-pip \
    cmake \
    build-essential \
    libopencv-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace/enhancex

COPY . .

RUN pip3 install --no-cache-dir --upgrade pip setuptools wheel
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install --no-cache-dir -e .

RUN mkdir build && cd build && \
    cmake .. -DCMAKE_BUILD_TYPE=Release -DENHANCEX_BUILD_CUDA=ON && \
    make -j$(nproc)

FROM nvidia/cuda:12.1.0-runtime-ubuntu22.04 AS final

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.10 \
    python3-pip \
    libopencv-core4.5d \
    libopencv-imgproc4.5d \
    libopencv-highgui4.5d \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/lib/python3.10/dist-packages /usr/local/lib/python3.10/dist-packages
COPY --from=builder /usr/local/bin/enhancex /usr/local/bin/enhancex
COPY --from=builder /workspace/enhancex /workspace/enhancex

WORKDIR /workspace/enhancex

ENTRYPOINT ["enhancex"]
CMD ["--help"]

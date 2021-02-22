FROM arm32v7/ubuntu:18.04

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y cmake ninja-build clang
RUN apt-get install -y libopencv-core-dev
RUN apt-get install -y git

WORKDIR /root

RUN git clone https://github.com/digitalbrain79/darknet-nnpack.git
RUN git clone https://github.com/shizukachan/NNPACK.git

RUN cd NNPACK && mkdir build && cd build && cmake -G Ninja -DBUILD_SHARED_LIBS=on .. && \
    ninja && ninja install

RUN apt-get install -y pkg-config g++
RUN echo 'APT::Acquire::Retries "3";' > /etc/apt/apt.conf.d/80-retries
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia
RUN apt-get install -y tzdata
RUN apt-get install -y libopencv-dev
RUN cd darknet-nnpack && \
    sed -i "/^OPENCV=0/c OPENCV=1" Makefile && \
    sed -i "/^LIBSO=0/c LIBSO=1" Makefile && \
    make
RUN apt-get install -y python3

COPY ./models /models


WORKDIR /root/darknet-nnpack
COPY ./darknet /root/darknet
#RUN cp /root/darknet-nnpack/darknet  /root/darknet/
#RUN cp /root/darknet-nnpack/libdarknet.so /root/darknet/
RUN cp /root/darknet/darknet.py /root/darknet-nnpack/
ENTRYPOINT ["python", "darknet.py"]





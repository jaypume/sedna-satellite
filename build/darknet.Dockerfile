FROM arm32v7/ubuntu:18.04

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y vim git python3
RUN apt-get install -y cmake ninja-build clang libopencv-core-dev  pkg-config g++

RUN echo 'APT::Acquire::Retries "3";' > /etc/apt/apt.conf.d/80-retries
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia
RUN apt-get install -y tzdata libopencv-dev

WORKDIR /root

RUN git clone https://github.com/digitalbrain79/darknet-nnpack.git
RUN git clone https://github.com/shizukachan/NNPACK.git

RUN cd NNPACK && mkdir build && cd build && cmake -G Ninja -DBUILD_SHARED_LIBS=on .. && \
    ninja && ninja install
RUN cd darknet-nnpack && \
    sed -i "/^OPENCV=0/c OPENCV=1" Makefile && \
    sed -i "/^LIBSO=0/c LIBSO=1" Makefile && \
    sed -i '488c printf("Bounding Box: Left=%d, Top=%d, Right=%d, Bottom=%d, %s: %.0f%%", left, top, right, bot, names[class_id], prob * 100);' src/image.c && \
    make

RUN ldconfig
RUN apt-get install -y python3-pip
RUN pip3 install Pillow

COPY ./models /models
COPY ./darknet /root/darknet
RUN cp /root/darknet-nnpack/darknet  /root/darknet/
WORKDIR /root/darknet
ENTRYPOINT ["python3", "main.py"]





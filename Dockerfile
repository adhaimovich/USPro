FROM ubuntu:16.04
FROM python:3.6

# Headless front-end, remove warnings
ARG DEBIAN_FRONTEND=noninteractive

# Get most recent updates
RUN apt-get update -qq

# ffmpeg: https://stackoverflow.com/questions/42589892/how-to-install-ffmpeg-for-ubuntu-using-command-line
RUN apt-get -y update && apt-get install -y wget nano git build-essential yasm pkg-config

# Compile and install ffmpeg from source
RUN git clone https://github.com/FFmpeg/FFmpeg /root/ffmpeg && \
    cd /root/ffmpeg && \
    ./configure --enable-nonfree --disable-shared --extra-cflags=-I/usr/local/include && \
    make -j8 && make install -j8

# If you want to add some content to this image because the above takes a LONGGG time to build
ARG CACHEBREAK=1

# Python scientific libraries
RUN pip3 --no-cache-dir install \
    numpy \
    scipy \
    scikit-learn \
    scikit-image \
    h5py \
    django \
    sk-video \
    SimpleITK

# Clean-up
RUN apt-get clean && apt-get autoremove \
 && rm -rf /var/lib/apt/lists/*

ADD . /USPro
WORKDIR /USPro

LABEL maintainer="Adrian <adrian dot haimovich at yale dot edu>"

EXPOSE 8000

# Permissions for entrypoint script
RUN ["chmod", "+x", "/USPro/docker_entrypoint.sh"]

# Assign entrypoint script
ENTRYPOINT ["/USPro/docker_entrypoint.sh"]


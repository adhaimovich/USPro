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

# Utils
RUN apt-get install -y --no-install-recommends apt-utils \
 && apt-get install -y --no-install-recommends \
    locales \
	ssh vim unzip less procps \
	git curl wget \
	build-essential g++ cmake \
 && echo 'Acquire::Retries "5";' > /etc/apt/apt.conf.d/99AcquireRetries \
 && sed -i 's/main$/main contrib non-free/' /etc/apt/sources.list
 
# Locales
ENV LANG="en_US.UTF-8" LANGUAGE="en_US:en" LC_ALL="en_US.UTF-8"

# Python (3.5)
# Aliases (but don't sym-link) python -> python3 and pip -> pip3
RUN apt-get install -y --no-install-recommends \
    python3 \
    python3-dev \
    python3-pip \
    python3-setuptools \
    #python3-virtualenv \
    pkg-config \
    # Required for keras
    python3-h5py \
    python3-yaml \
    python3-pydot

# Upgrade with latest pip and create aliases
RUN pip3 install --no-cache-dir --upgrade pip setuptools \
 && echo "alias python='python3'" >> /root/.bash_aliases \
 && echo "alias pip='pip3'" >> /root/.bash_aliases


## Python scientific libraries
RUN pip3 --no-cache-dir install \
    numpy \
    scipy \
    scikit-learn \
    scikit-image \
    pydicom \
    h5py \
    django \
    imageio \
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


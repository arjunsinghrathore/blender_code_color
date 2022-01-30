FROM nvidia/cuda:8.0-runtime

MAINTAINER Phil Bayer <philip_bayer@brown.edu>
LABEL authors="Phil Bayer <philip_bayer@brown.edu>"

RUN apt-get update && \
    apt-get install -y \
        curl \
        bzip2 \
        libfreetype6 \
        libgl1-mesa-dev \
        libglu1-mesa \
        libxi6 \
        libxrender1 \
        python \
        python-dev \
        python-pip \
        python-virtualenv && \
    apt-get -y autoremove && \
    rm -rf /var/lib/apt/lists/*

ENV BLENDER_MAJOR 2.79
ENV BLENDER_VERSION 2.79
ENV BLENDER_BZ2_URL https://mirror.clarkson.edu/blender/release/Blender$BLENDER_MAJOR/blender-$BLENDER_VERSION-linux-glibc219-x86_64.tar.bz2

RUN mkdir /usr/local/blender && \
    curl -SL "$BLENDER_BZ2_URL" -o blender.tar.bz2 && \
    tar -jxvf blender.tar.bz2 -C /usr/local/blender --strip-components=1 && \
    rm blender.tar.bz2

VOLUME /media/data_cifs

# Get pip to download and install requirements:
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy entire repository
COPY . .

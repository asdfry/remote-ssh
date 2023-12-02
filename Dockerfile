FROM python:3.10.6-slim

SHELL ["/bin/bash", "-c"]

USER root

WORKDIR /root

ENV DEBIAN_FRONTEND=noninteractive

# Install packages
RUN apt-get update && \
    apt-get install -y curl pdsh vim net-tools git tmux

# Install python & pip and Install libraries
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python3 get-pip.py && \
    pip install paramiko==3.3.1

# For util
RUN echo "alias ll='ls -al'" >> ~/.bashrc

# Copy files
COPY servers.txt servers.txt
COPY remote_ssh.py remote_ssh.py

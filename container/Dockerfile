FROM registry.access.redhat.com/ubi9/ubi:9.3

USER root

# setup: coder user
RUN mkdir /home/coder && \
    chgrp -R 0 /home/coder && \
    chmod -R g=u /home/coder

COPY repo-files /etc/yum.repos.d/

RUN rpm --import http://mirror.centos.org/centos/RPM-GPG-KEY-CentOS-Official && \
    dnf -y update --disablerepo=CentOS* --setopt=install_weak_deps=False && \
    dnf -y install --disablerepo=CentOS* --setopt=install_weak_deps=False \
    gnupg bind-utils \
    git gcc gcc-c++ cmake make \
    python3 python3-pip \
    pkg-config \
    bash-completion rsync zip unzip \
    nano vim jq \
    python3-devel \
    zlib-devel bzip2 bzip2-devel \
    sqlite sqlite-devel openssl-devel \
    libffi-devel xz-devel && \
    dnf -y install --disablerepo=* --enablerepo=CentOS* --setopt=install_weak_deps=False \
    tk-devel readline-devel \
    zsh glibc-langpack-en \
    unixODBC && \
    dnf clean all && \
    rm -rf /var/cache /var/log/dnf* /var/log/yum.* && \
    chmod g+w /etc/passwd && \
    ln -s /usr/bin/python3 /usr/local/bin/python && \
    ln -s /usr/bin/pip3 /usr/local/bin/pip

USER coder

ENV HOME=/home/coder

WORKDIR /home/coder
VOLUME /home/coder
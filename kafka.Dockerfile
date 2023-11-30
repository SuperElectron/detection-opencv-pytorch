# syntax = docker/dockerfile:1.2
FROM ubuntu:22.04
LABEL maintainer="Matthew McCann <matmccann@gmail.com>"
USER root

ENV DEBIAN_FRONTEND noninteractive
ENV JAVA_HOME /usr/lib/jvm/java-1.8.0-openjdk-amd64
EXPOSE 22 2181 2888 3888 9200

# versions for kafka download
ENV KAFKA_VERSION 3.6.0
ENV SCALA_VERSION 2.13

RUN export PATH=$JAVA_HOME/bin:$PATH
RUN rm -f /etc/apt/apt.conf.d/docker-clean

# install apt packages
RUN --mount=type=cache,target=/var/cache/apt apt-get update -yqq && \
    apt-get install -yqq --no-install-recommends \
    bash vim unzip curl iputils-ping netcat tmux \
    openjdk-8-jdk \
    openssh-server apache2 supervisor \
    && rm -rf /var/lib/apt/lists/*

# Install kafka and copy configs
RUN cd /tmp && \
  curl -OL "https://downloads.apache.org/kafka/${KAFKA_VERSION}/kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz" && \
  tar -zxf "kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz" && \
  mv kafka_${SCALA_VERSION}-${KAFKA_VERSION} /opt/kafka

COPY ./.build/kafka-server.properties /opt/kafka/config/server.properties
COPY ./.build/zookeeper.properties /opt/kafka/config/zookeeper.properties

# Setup supervisord to run kafka and zookeeper processes
COPY ./.build/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
RUN mkdir -p /var/lock/apache2 /var/run/apache2 /var/run/sshd /var/log/supervisor

# Set up docker for runtime
RUN rm -rf /tmp/start
WORKDIR "/opt/kafka"
HEALTHCHECK CMD "echo stat | nc 127.0.0.1 2181"
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
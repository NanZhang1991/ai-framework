FROM centos:centos7.9.2009

# 如果需要cuda 环境请使用对应的cuda镜像
#FROM yeluofeng1991/cuda:11.2-centos7.9

USER root

ENV TZ=Asia/Shanghai
ENV LANG C.UTF-8

RUN curl -o /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo

ENV PYTHON_VERSION 3.7.9
#  Dependencies required to install Python Otherwise, the pip3 package will not be installed
RUN yum update -y
RUN yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel libffi-devel gcc make lzma

WORKDIR /home

# Insatll redis
RUN set -ex &&\
        curl https://download.redis.io/redis-stable.tar.gz -o redis-stable.tar.gz && \
        tar -xvzf redis-stable.tar.gz && \
        mv redis-stable/ redis && \
        rm -f redis-stable.tar.gz && \
        yum clean all && \
        cd redis && \
        make && make PREFIX=/usr/local/redis install && \
        mkdir -p /usr/local/redis/conf/ && \
        cp /home/redis/redis.conf  /usr/local/redis/conf/  && \
        rm -rf /home/redis && \
        sed -i '69s/127.0.0.1/0.0.0.0/' /usr/local/redis/conf/redis.conf && \
        sed -i '88s/protected-mode yes/protected-mode no/' /usr/local/redis/conf/redis.conf

ENV PATH=$PATH:/usr/local/redis/bin

# insatll python
RUN set -ex \
        && curl -fSL "https://npm.taobao.org/mirrors/python/${PYTHON_VERSION%%[a-z]*}/Python-$PYTHON_VERSION.tar.xz" -o python.tar.xz \
        && export GNUPGHOME="$(mktemp -d)" \
        && mkdir -p /usr/src/python \
        && tar -xJC /usr/src/python --strip-components=1 -f python.tar.xz \
        && rm python.tar.xz \
        && cd /usr/src/python \
        && ./configure --prefix=/usr/local/python3 \
        && make && make install \
        && ln -s /usr/local/python3/bin/python3 /usr/bin/python3 \
        && ln -s /usr/local/python3/bin/pip3 /usr/bin/pip3 \
        && pip3 config set global.index-url https://pypi.douban.com/simple  \
        && pip3 config set install.trusted-host pypi.douban.com \
        && pip3 config set global.ssl_verify false \
        && pip3 install --upgrade pip

# 克隆代码
RUN yum install git -y && \
        git clone -b develop https://zhangnan:forp-zhangnan@git.apexsoft.com.cn/forp/YFB/AI-GROUP/AI-MODEL/FRAMEWORK/ai-framework.git

WORKDIR /home/ai-framework
RUN set -ex \
    && pip3 install -r requirements.txt

#celery
RUN set -ex \
       && ln -s /usr/local/python3/bin/celery /usr/bin/celery

RUN chmod 777 env/run.sh


CMD env/run.sh

# CMD redis-server /usr/local/redis/conf/redis.conf &\
#     celery -A app.celery_app.task worker --loglevel=info &\
#     python3 server.py


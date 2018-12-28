FROM python:3.6
# Mecab　環境
ENV LANG C.UTF-8

RUN apt update \
    && apt install -y mecab \
    && apt install -y libmecab-dev \
    && apt install -y mecab-ipadic-utf8\
    && apt install -y git\
    && apt install -y make\
    && apt install -y curl\
    && apt install -y xz-utils\
    && apt install -y file\
    && apt install -y sudo\
    && apt install -y wget\
    && apt install -y swig

RUN git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git\
    && cd mecab-ipadic-neologd\
    && bin/install-mecab-ipadic-neologd -n -y

RUN apt install -y software-properties-common vim
RUN apt update

RUN pip install pipenv
# For include .venv/ in project
ENV  PIPENV_VENV_IN_PROJECT 1

ENV APP_HOME /scripts
RUN mkdir $APP_HOME
WORKDIR $APP_HOME
ADD . $APP_HOME
FROM python:3.7.6-slim-buster

WORKDIR /workdir

RUN mkdir -p repos conf scripts nltk_data notebooks

ARG DEBIAN_FRONTEND=noninteractive

ENV ARTM_SHARED_LIBRARY /usr/local/lib/libartm.so
ENV NLTK_DATA /workdir/nltk_data
ENV TREE_SITTER_LANGUAGES_SO /workdir/tree-sitter-languages.so
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  apt-utils \
  ca-certificates \
  curl \
  locales \
  && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
  && locale-gen \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

COPY conf/requirements-bigartm.txt conf/
COPY conf/requirements-tree-sitter.txt conf/
COPY scripts/install-bigartm scripts/
COPY scripts/*tree-sitter* scripts/
COPY scripts/install-nltk-data scripts/

RUN ./scripts/install-bigartm \
  && ./scripts/install-tree-sitter \
  && ./scripts/install-nltk-data \
  && pip3 install --no-cache-dir "jupyter == 1.0.0" \
  && pip3 install --no-cache-dir \
  "jupyter_contrib_nbextensions == 0.5.1" \
  "jupyter_nbextensions_configurator == 0.4.1" \
  && jupyter contrib nbextension install \
  && jupyter nbextensions_configurator enable

COPY conf/jupyter-notebook-config.json /root/.jupyter/nbconfig/notebook.json
COPY conf/jupyter-server-config.json /root/.jupyter/jupyter_notebook_config.json

COPY conf/requirements-setup.txt conf/
COPY conf/requirements.txt conf/

RUN pip3 install --no-cache-dir -r conf/requirements-setup.txt \
  && pip3 install --no-cache-dir -r conf/requirements.txt

WORKDIR /workdir/notebooks

ENTRYPOINT jupyter notebook --ip 0.0.0.0 --allow-root --no-browser

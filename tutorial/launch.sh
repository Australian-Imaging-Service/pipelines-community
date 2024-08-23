#!/usr/bin/env bash

set -e

PIPELINES_REPO_DIR=$(pwd)/$(dirname $0)/..

if [ -z $(docker volume ls | grep docker ais-pipelines-tutorial-home) ]; then
    docker volume create ais-pipelines-tutorial-home
fi

docker run \
  --shm-size=1gb -it --privileged --user=root --name ais-pipelines-tutorial \
  --mount source=ais-pipelines-tutorial-home,target=/home/jovyan \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v ${PIPELINES_REPO_DIR}:/home/jovyan/git/pipelines-community \
  -e NB_UID="$(id -u)" -e NB_GID="$(id -g)" \
  -p 8888:8888 \
  -p 8080:8080 \
  -e NEURODESKTOP_VERSION=2024-05-25 ghcr.io/ais-pipelines-tutorial:latest > out.txt

  JUPYTER_PATH=$(grep http://localhost < out.txt | awk '{print $1}')

  open $JUPYTER_PATH
  
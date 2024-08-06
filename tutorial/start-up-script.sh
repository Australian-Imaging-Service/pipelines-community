#!/usr/bin/env bash

# Clone the pipelines-community repository
mkdir -p ~/git
if [ ! -d ~/git/pipelines-community ]; then
    git clone git@github.com:Australian-Imaging-Service/pipelines-community.git ~/git/pipelines-community
fi
pushd ~/git/pipelines-community

# Update the pipelines-community repository
git pull

# Install the pipelines-community repository
pip install -r ./tutorial/requirements.txt

# Pre-build the XNAT docker image to save time
xnat4tests -c ./tutorial/xnat4tests-config.yaml start --with-data openneuro-t1w
xnat4tests -c ./tutorial/xnat4tests-config.yaml stop
popd
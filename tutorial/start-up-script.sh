#!/usr/bin/env bash

ssh-keygen -t rsa -N "" -f $HOME/.ssh/id_rsa.pub

# Clone the pipelines-community repository
mkdir -p ~/git
if [ ! -d ~/git/pipelines-community ]; then
    git clone https://github.com/Australian-Imaging-Service/pipelines-community.git ~/git/pipelines-community
fi
pushd ~/git/pipelines-community

# Update the pipelines-community repository
git pull

# Install the pipelines-community repository
pip install -r ./tutorial/requirements.txt

# Pre-build/pull the required XNAT docker images to save time
xnat4tests -c ./tutorial/xnat4tests-config.yaml start --with-data openneuro-t1w
xnat4tests -c ./tutorial/xnat4tests-config.yaml stop
pydra2app make xnat ./specs/australian-imaging-service-community/examples/zip.yaml --spec-root ./specs  --for-localhost
pydra2app make xnat ./specs/australian-imaging-service-community/examples/bet.yaml --spec-root ./specs  --for-localhost
docker pull vnmd/freesurfer_7.1.1
popd
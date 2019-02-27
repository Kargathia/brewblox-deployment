#! /bin/bash

source ./vars.sh
mkdir -p repodir
cd repodir

for repo in ${REPOS}; do
    git clone https://github.com/BrewBlox/${repo}.git
done

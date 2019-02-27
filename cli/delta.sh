#! /bin/bash

source ./vars.sh

for repo in ${REPOS}; do
    pushd repodir/${repo} > /dev/null
    git fetch --tags > /dev/null
    DEV_EDGE=$(git rev-list --count origin/edge..origin/develop)
    EDGE_TAG=$(git rev-list --count $(git describe --tags $(git rev-list --tags --max-count=1))..origin/edge)
    echo $repo
    echo "  +${DEV_EDGE} +${EDGE_TAG} (develop > edge > tag)"
    popd > /dev/null
done

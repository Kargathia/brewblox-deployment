#!/usr/bin/env bash
set -e

DOCKER_REPOS=" \
brewblox-devcon-spark \
brewblox-history \
brewblox-mdns \
brewblox-ui \
firmware-flasher \
"

for repo in ${DOCKER_REPOS}; do
    docker pull brewblox/${repo}:newest-tag
    docker pull brewblox/${repo}:rpi-newest-tag
done

for repo in ${DOCKER_REPOS}; do
    docker tag brewblox/${repo}:newest-tag brewblox/${repo}:stable
    docker push brewblox/${repo}:stable
    docker tag brewblox/${repo}:rpi-newest-tag brewblox/${repo}:rpi-stable
    docker push brewblox/${repo}:rpi-stable
done

docker pull brewblox/firmware-simulator:newest-tag
docker tag brewblox/firmware-simulator:newest-tag brewblox/firmware-simulator:stable
docker push brewblox/firmware-simulator:stable

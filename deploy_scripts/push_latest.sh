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
    docker pull brewblox/${repo}:stable
    docker pull brewblox/${repo}:rpi-stable
done

for repo in ${DOCKER_REPOS}; do
    docker tag brewblox/${repo}:stable brewblox/${repo}:latest
    docker push brewblox/${repo}:latest
    docker tag brewblox/${repo}:rpi-stable brewblox/${repo}:rpi-latest
    docker push brewblox/${repo}:rpi-latest
done

docker pull brewblox/firmware-simulator:stable
docker tag brewblox/firmware-simulator:stable brewblox/firmware-simulator:latest
docker push brewblox/firmware-simulator:latest

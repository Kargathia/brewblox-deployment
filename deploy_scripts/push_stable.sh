#!/usr/bin/env bash
set -e

AMD_ARM_REPOS=" \
brewblox/brewblox-devcon-spark \
brewblox/brewblox-history \
brewblox/brewblox-mdns \
brewblox/brewblox-ui \
brewblox/firmware-flasher \
brewblox/brewblox-ctl-lib \
"

AMD_REPOS=" \
brewblox/firmware-simulator \
"

for repo in ${AMD_ARM_REPOS}; do
    docker pull ${repo}:newest-tag
    docker pull ${repo}:rpi-newest-tag
done

for repo in ${AMD_REPOS}; do
    docker pull ${repo}:newest-tag
done

# Re-tag and push if everything could be pulled OK

for repo in ${AMD_ARM_REPOS}; do
    docker tag ${repo}:newest-tag ${repo}:stable
    docker push ${repo}:stable
    docker tag ${repo}:rpi-newest-tag ${repo}:rpi-stable
    docker push ${repo}:rpi-stable
done

for repo in ${AMD_REPOS}; do
    docker tag ${repo}:newest-tag ${repo}:stable
    docker push ${repo}:stable
done

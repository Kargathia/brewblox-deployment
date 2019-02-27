#! /bin/bash
VERSION=2.10.0

# Install binary and documentation
wget https://github.com/github/hub/releases/download/v${VERSION}/hub-linux-amd64-${VERSION}.tgz
tar zvxvf hub-linux-amd64-${VERSION}.tgz
sudo ./hub-linux-amd64-${VERSION}/install

# Cleanup
rm -rf hub-linux-amd64-${VERSION}*

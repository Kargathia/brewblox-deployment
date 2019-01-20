# BrewBlox Deployment

This repository contains:
* Integration tests
* Default configuration files
* Docker base images

A guide for installing BrewBlox can be found [here](https://brewblox.netlify.com/user/startup.html).

## Integration tests

The integration tests start a BrewBlox environment using docker-compose, and then run their tests against the exposed REST API's.

To run:
```bash
cd integration
docker-compose pull
bash run.sh
```

Afterwards, logs for relevant services can be found in `integration/logs`.

## Default configuration files

Configuration files are downloaded by the BrewBlox [install script](https://brewblox.netlify.com/install). The install script will download two parts:

* architecture-specific files in either `amd64` or `armhf`
* generic files in `shared`

## Docker base images

As described in [design decisions: base images](https://brewblox.netlify.com/dev/decisions/crosscompilation_base_images.html), we are using our own Docker base images for the Raspberry Pi architecture.

The scripts to generate them are placed in `base_images/`. These scripts should only be re-run if there are any upstream updates to the relevant images.

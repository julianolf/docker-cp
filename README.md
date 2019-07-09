# docker-cp
[![Build Status](https://travis-ci.com/julianolf/docker-cp.svg?branch=master)](https://travis-ci.com/julianolf/docker-cp) [![codecov](https://codecov.io/gh/julianolf/docker-cp/branch/master/graph/badge.svg)](https://codecov.io/gh/julianolf/docker-cp) [![Updates](https://pyup.io/repos/github/julianolf/docker-cp/shield.svg)](https://pyup.io/repos/github/julianolf/docker-cp/) [![Python 3](https://pyup.io/repos/github/julianolf/docker-cp/python-3-shield.svg)](https://pyup.io/repos/github/julianolf/docker-cp/) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black) [![GitHub](https://img.shields.io/github/license/julianolf/docker-cp.svg)](https://opensource.org/licenses/MIT)

> A simple program for the command line that allows copying files between a Docker container and its host.

### Requirements
- Python 3.6+ (3.7 recommended)
- Pip
- Setuptools

## Installation
First, get a copy of the source code, you can download the zip file and extract the content or clone the repository using Git. To clone the repository open a terminal application and type the following command:

```sh
$ git clone https://github.com/julianolf/docker-cp.git
```

Then, navigate to the project's directory and execute the installation:

```sh
$ cd path/to/docker-cp
$ python setup.py install
```

After the installation finished you can confirm the version and usage by typing:

```sh
$ docker-cp --version
0.1.0a1

$ docker-cp
Usage:
    docker-cp [--buffer-length=<bytes>] FILE TARGET
    docker-cp (-h | --help)
    docker-cp --version
```

## Development
The configuration of the development environment requires the installation of a few extra Python packages. Open a terminal application, navigate to the project's directory and execute the following commands:

```sh
$ cd path/to/docker-cp
$ pip install pipenv --upgrade
$ pipenv sync -d
```

Now, run the tests just to confirm that everything is in place:

```sh
$ pipenv run tests
```

## Note

This project was developed as part of my application for a software engineer position and it's not meant to be used for any other purpose than a study case.

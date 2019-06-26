# docker-cp
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

## Tests
The software was tested with the following environment configurations:

- Mac
  - macOS Mojave 10.14.5
  - Docker 18.0.2
  - Python 3.7.3
  - Pip 19.1.1
  - Setuptools 41.0.1
- Linux
  - CentOS 7.6.1810
  - Docker 18.09.6
  - Python 3.6.3
  - Pip 19.1.1
  - Setuptools 41.0.1
- Travis CI
  - Ubuntu Xenial 16.04.6 LTS
  - Docker ?
  - Python 3.7.3
  - Pip 19.0.3
  - Setuptools 40.8.0

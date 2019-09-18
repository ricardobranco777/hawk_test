# hawk_test

This Docker image runs a set of Selenium tests for testing [Hawk](https://github.com/ClusterLabs/hawk/)

[![Build Status](https://travis-ci.org/ricardobranco777/hawk_test.svg?branch=master)](https://travis-ci.org/ricardobranco777/hawk_test)

## Usage

```
Usage: hawk_test.py [-h] -b {firefox,chrome,chromium} [-H HOST]
                    [-I VIRTUAL_IP] [-P PORT] [-p PREFIX] -t TEST_VERSION
                    [-s SECRET] [-r RESULTS]
```

## Dependencies

- OS packages:
  - Xvfb
  - Firefox
  - [Geckodriver](https://github.com/mozilla/geckodriver/releases)
  - Chromium (optional)
  - [Chromedriver](https://chromedriver.chromium.org/downloads) (optional)
  - Python 3
- Python packages:
  - paramiko
  - selenium
  - PyVirtualDisplay

## Usage with Docker

Build image with:

`docker build -t hawk_test -f Dockerfile.alpine`

First you must create a world-writable directory (with the sticky bit set for security):

`mkdir -m 1777 test/`

Run:

```docker run --ipc=host -xvfb -v $PWD/test:/test hawk_test [OPTIONS]```

If you don't want to use the Xvfb headless mode:

```
xhost +
docker run --ipc=host -e DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v $PWD/test:/test hawk_test [OPTIONS]
```

Notes:
  - You may want to add `--net=host` if you have problems with DNS resolution.

## Options

```
  -b {firefox,chrome,chromium}, --browser {firefox,chrome,chromium}
                        Browser to use in the test
  -H HOST, --host HOST  Host or IP address where HAWK is running
  -I VIRTUAL_IP, --virtual-ip VIRTUAL_IP
                        Virtual IP address in CIDR notation
  -P PORT, --port PORT  TCP port where HAWK is running
  -p PREFIX, --prefix PREFIX
                        Prefix to add to Resources created during the test
  -t TEST_VERSION, --test-version TEST_VERSION
                        Test version. Ex: 12-SP3, 12-SP4, 15, 15-SP1
  -s SECRET, --secret SECRET
                        root SSH Password of the HAWK node
  -r RESULTS, --results RESULTS
                        Generate hawk_test.results file
  --xvfb                Use Xvfb. Headless mode
```

## FAQ

- Why Xvfb?
  - The `-headless` in both browsers still have bugs, specially with modal dialogs.
  - Having Xvfb prevents it from connecting to our X system.
- Why docker?
  - The Docker image packs the necessary dependencies in such a way that fits the compatibility matrix between Python, Selenium, Firefox (and Geckodriver) & Chromium (and Chromedriver).

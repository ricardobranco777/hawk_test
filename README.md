# hawk_test

This Docker image runs a set of Selenium tests for testing [Hawk](https://github.com/ClusterLabs/hawk/)

[![Build Status](https://travis-ci.org/ricardobranco777/hawk_test.svg?branch=master)](https://travis-ci.org/ricardobranco777/hawk_test)

## Usage

```
usage: hawk_test.py [-h] [-b {firefox,chrome,chromium}] [-H HOST] [-S SLAVE]
                    [-I VIRTUAL_IP] [-P PORT] [-p PREFIX] -t TEST_VERSION
                    [-s SECRET] [-r RESULTS] [--xvfb]

```

## Dependencies

- OS packages:
  - Xvfb (optional)
  - Docker (optional)
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

Run:

```docker run --ipc=host -xvfb hawk_test [OPTIONS]```

If you don't want to use the Xvfb headless mode:

```
xhost +
docker run --ipc=host -e DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix hawk_test [OPTIONS]
```

Notes:
  - You may want to add `--net=host` if you have problems with DNS resolution.

## Options

```
  -h, --help            show this help message and exit
  -b {firefox,chrome,chromium}, --browser {firefox,chrome,chromium}
                        Browser to use in the test
  -H HOST, --host HOST  Host or IP address where HAWK is running
  -S SLAVE, --slave SLAVE
                        Host or IP address of the slave
  -I VIRTUAL_IP, --virtual-ip VIRTUAL_IP
                        Virtual IP address in CIDR notation
  -P PORT, --port PORT  TCP port where HAWK is running
  -p PREFIX, --prefix PREFIX
                        Prefix to add to Resources created during the test
  -t TEST_VERSION, --test-version TEST_VERSION
                        Test SLES Version. Ex: 12-SP3, 12-SP4, 15, 15-SP1
  -s SECRET, --secret SECRET
                        root SSH Password of the HAWK node
  -r RESULTS, --results RESULTS
                        Generate hawk_test.results file for use with openQA.
  --xvfb                Use Xvfb. Headless mode
```

## FAQ

- Why Xvfb?
  - The `-headless` in both browsers still have bugs, specially with modal dialogs.
  - Having Xvfb prevents it from connecting to our X system.
- Why docker?
  - The Docker image packs the necessary dependencies in such a way that fits the compatibility matrix between Python, Selenium, Firefox (and Geckodriver) & Chromium (and Chromedriver).

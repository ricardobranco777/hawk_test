FROM	registry.opensuse.org/opensuse/leap

RUN	zypper -n install python3 python3-pip firefox chromium shadow xdpyinfo xorg-x11-server && \
	zypper -n clean -a

COPY    requirements.txt /tmp
RUN	pip install --no-cache-dir -r /tmp/requirements.txt

ADD	https://github.com/mozilla/geckodriver/releases/download/v0.25.0/geckodriver-v0.25.0-linux64.tar.gz /usr/local/bin/

RUN	useradd -l -m -d /test test

COPY	*.py /

ENV     PYTHONPATH /
ENV	PYTHONUNBUFFERED 1
ENV	DBUS_SESSION_BUS_ADDRESS /dev/null

WORKDIR	/test

USER	test
ENTRYPOINT ["/usr/bin/python3", "/hawk_test.py"]

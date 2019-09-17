FROM	python:3.7-alpine

COPY    requirements.txt /tmp

RUN     apk --no-cache --virtual .build-deps add \
                gcc \
                libc-dev \
                libffi-dev \
                make \
                openssl-dev && \
	apk add --no-cache \
		chromium \
		chromium-chromedriver \
		firefox-esr \
		tzdata \
		xdpyinfo \
		xvfb && \
        pip install --no-cache-dir -r /tmp/requirements.txt && \
        apk del .build-deps

ADD     https://github.com/mozilla/geckodriver/releases/download/v0.25.0/geckodriver-v0.25.0-linux64.tar.gz /usr/local/bin/

RUN	adduser -D test -h /test

COPY	*.py /
RUN	python -OO -m compileall && \
	python -OO -m compileall /*.py

ENV     PYTHONPATH /
ENV	PYTHONUNBUFFERED 1
ENV	DBUS_SESSION_BUS_ADDRESS /dev/null

WORKDIR	/test

USER	test
ENTRYPOINT ["/usr/local/bin/python3", "/hawk_test.py"]

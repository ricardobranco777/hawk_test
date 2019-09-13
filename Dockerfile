FROM	python:3.7-alpine

COPY    requirements.txt /tmp

RUN     apk --no-cache --virtual .build-deps add \
                gcc \
                libc-dev \
                libffi-dev \
                make \
                openssl-dev && \
	apk add --no-cache \
		firefox-esr \
		tzdata \
		xdpyinfo \
		xvfb && \
        pip install --no-cache-dir -r /tmp/requirements.txt && \
        ln -s /usr/local/bin/python3 /usr/bin/python3 && \
        apk del .build-deps

RUN	wget -q -O- https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz | tar zxf - -C /usr/local/bin/

RUN	adduser -D test

COPY	*.py /home/test/
RUN	chown -R test.test /home/test
RUN	chmod +x /home/test/hawk_test.py

ENV     PYTHONPATH .
ENV	PYTHONUNBUFFERED 1
ENV	DBUS_SESSION_BUS_ADDRESS /dev/null

WORKDIR	/home/test

USER	test
ENTRYPOINT ["/home/test/hawk_test.py"]

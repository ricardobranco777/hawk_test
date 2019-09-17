test:
	@flake8 --ignore=E501&& \
	pylint --ignored-modules=distutils *.py

test-docker:
	@docker build -t hawk_test . && \
	docker run --rm hawk_test --help

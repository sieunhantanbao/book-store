.ONESHELL:

.PHONY: clean install tests run all

clean:
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.log' -delete

install:
	virtualenv venv; \
	.venv/Scripts/activate; \
	pip install -r requirements.txt;

tests:
	.venv/Scripts/activate; \
	python main.py test

run:
	.venv/Scripts/activate; python main.py;

all: clean install tests run
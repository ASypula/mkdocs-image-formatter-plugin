.ONESHELL:

PYTHON = ./venv/bin/python3
PIP = ./venv/bin/pip

tests:
	pytest

pre_commit:
	tox

venv/bin/activate: requirements.txt
	python3 -m venv venv
	chmod +x venv/bin/activate
	. ./venv/bin/activate
	$(PIP) install -r requirements.txt

setup: venv/bin/activate

clean:
	rm -rf __pycache__
	rm -rf venv
	rm -rf .tox

.PHONY: tests clean pre_commit
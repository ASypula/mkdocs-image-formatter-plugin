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

setup_venv: venv/bin/activate

setup:
	$(PIP) install -r requirements.txt

clean:
	rm -rf __pycache__
	rm -rf venv
	rm -rf .tox
	rm -rf .hypothesis

demo_cats:
	cd demo/demo_cats
	mkdocs serve

demo_dogs:
	cd demo/demo_dogs
	mkdocs serve

.PHONY: tests clean pre_commit
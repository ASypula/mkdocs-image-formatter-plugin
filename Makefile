tests:
	pytest

pre_commit:
	pytest .
	black . -l 120

clean:
	rm -rf __pycache__

setup:
	python3.10 -m venv venv
	source venv/bin/activate
	pip install -r requirements.txt

.PHONY: tests clean pre_commit
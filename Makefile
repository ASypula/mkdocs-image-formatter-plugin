tests:
	pytest

clean:
	rm -rf __pycache__

.PHONY: tests clean
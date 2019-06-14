setup:
	python3 -m venv ~/.gcp-real-estate-app

install:
	pip install -r ~/requirements.txt

test:
	#python -m pytest -vv --cov=main.py main_test.py

lint:
	pylint --disable=R,C templates *.py

all: install lint test

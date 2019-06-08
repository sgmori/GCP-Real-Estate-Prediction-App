setup:
	python3 -m venv ~/.gcp-real-estate-app

install:
	pip install -r requirements.txt

test:
	python -m pytest -vv *.py
	#PYTHONPATH=. && py.test --nbval-lax notebooks/*.ipynb

lint:
	pylint --disable=R,C *

all: install lint test

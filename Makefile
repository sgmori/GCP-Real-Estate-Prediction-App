setup:
	python3 -m venv ~/.gcp-real-estate-app

install:
	pip install -r ~/RE-Pred-App/requirements.txt

test:
	python -m pytest -vv --cov=RE-Pred-App RE-Pred-App/*.py
	#PYTHONPATH=. && py.test --nbval-lax notebooks/*.ipynb

lint:
	pylint --disable=R,C RE-Pred-App

all: install lint test

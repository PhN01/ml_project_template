init:
	python -m venv env
	. env/bin/activate
	pip install -r requirements.txt
	# pip list

activate_env:
	. env/bin/activate

lint: activate_env
	isort .
	black .
	flake8 .
	mypy .

lint-test: activate_env
	isort . --check-only
	flake8 .
	mypy .

test: lint-test
	coverage run
	coverage report

git-test: activate_env
	coverage run
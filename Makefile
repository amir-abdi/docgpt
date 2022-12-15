black:
	black .

black-check:
	black --check .

mypy:
	mypy docgpt

pylint:
	pylint docgpt

pytest:
	pytest .

all: black-check mypy pylint pylint pytest

black:
	black .

black-check:
	black --check .

mypy:
	mypy pydoc_gpt

pylint:
	pylint pydoc_gpt

test:
	pytest .


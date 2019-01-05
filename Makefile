.PHONY: tests

run:
	@#https://github.com/huge-success/sanic/issues/1248
	@PYTHONPATH="$(PYTHONPATH):$(PWD)/betbright" python -m betbright.server

tests:
	@ENV="test" pytest tests/ -p no:cacheprovider --flake8 .

setup:
	@pip install -r test-requirements.txt

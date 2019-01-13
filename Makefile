.PHONY: tests

run-server:
	@#https://github.com/huge-success/sanic/issues/1248
	@PYTHONPATH="$(PYTHONPATH):$(PWD)/betbright" python -m betbright.server

run-worker:
	@python -m betbright.worker

tests:
	@ENV="test" pytest tests/ -p no:cacheprovider --flake8 .

setup:
	@pip install -r test-requirements.txt

.DEFAULT_GOAL := test

run:
	pipenv run python dump_system_metrics.py | tee output.json

test:
	pipenv run python -m pytest .

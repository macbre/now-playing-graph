coverage_options = --include='now_playing_graph/*' --omit='test/*'

install:
	pip install -e .[dev]

test:
	pytest -vv

coverage:
	rm -f .coverage*
	rm -rf htmlcov/*
	coverage run -p -m pytest -vv
	coverage combine
	coverage html -d htmlcov $(coverage_options)
	coverage xml -i
	coverage report $(coverage_options)

lint:
	pylint now_playing_graph

.PHONY: test

# DEMO: this file is irrelevant for the POC, I am not going to suggest any changes to how me manage
# local dev env tasks
build:
	docker-compose build

up:
	docker-compose up

test-watch:
	docker-compose run -e MONGODB_URL=mongodb://mongodb:27017/authal_test --rm authal poetry run pytest-watch -v

fixes:
	docker-compose run authal poetry run isort -rc authal tests
	docker-compose run -e MONGODB_URL=mongodb://mongodb:27017/authal_test --rm authal poetry run pytest -vv --cov=authal --ignore=authal --cov-report=term-missing --cov-report=xml
	docker-compose down

test:
	docker-compose run authal poetry run isort -rc authal tests --check-only
	docker-compose run authal poetry run flake8 authal
	docker-compose run authal poetry run mypy authal tests
	docker-compose run -e MONGODB_URL=mongodb://mongodb:27017/authal_test --rm authal poetry run pytest -vv --cov=authal --ignore=authal --cov-report=term-missing --cov-report=xml
	docker-compose down

down:
	docker-compose down

.phony: build up test-watch fixes test down

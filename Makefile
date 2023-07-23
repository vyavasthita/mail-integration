NAME := Mail Integration
REPO_URL=https://github.com/vyavasthita/mail-integration
BUILD_ENV ?= development
.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo "Welcome to $(NAME)!"
	@echo "Use 'make <target>' where <target> is one of:"
	@echo ""
	@echo "  all		run stop -> up"
	@echo "  test		run test"
	@echo "  testcov	run testcov"
	@echo "  clean		clear network, container and images"
	@echo "  build		build container images"
	@echo "  up		run containers"
	@echo "  start		start containers"
	@echo "  restart	restart containers"
	@echo "  stop		stop containers"
	@echo "  down		bring down containers"
	@echo "  logs		show logs of containers"
	@echo "  ps		show container status"
	@echo "  destroy	destroy containers"
	@echo "  test	run automated tests"
	@echo ""
	@echo "Choose one option!"

ifeq ($(BUILD_ENV),qa)
 $(info qa)
 ENV_FILE=configuration/qa/.env.app
 COMPOSE_FILE=docker-compose.qa.yaml
else ifeq ($(BUILD_ENV), production)
$(info production)
 ENV_FILE=configuration/production/.env.app
 COMPOSE_FILE=docker-compose.prod.yaml
else
 $(info development)
 ENV_FILE=configuration/development/.env.app
 COMPOSE_FILE=docker-compose.dev.yaml
endif

TEST_ENV_FILE=configuration/.env.test

test: test
testcov: testcov
all: stop up

.PHONY: clean
clean: ## clear network, container and images
	docker network prune -f
	docker container prune -f
	docker image prune -f
.PHONY: build
build: ## build container images
	docker compose --env-file $(ENV_FILE) -f $(COMPOSE_FILE) build --no-cache
.PHONY: up
up: ## run containers
	docker compose --env-file $(ENV_FILE) -f $(COMPOSE_FILE) up -d --build --remove-orphans
.PHONY: start
start: ## start containers
	docker compose --env-file $(ENV_FILE) -f $(COMPOSE_FILE) start
.PHONY: restart
restart: ## restart containers
	docker compose --env-file $(ENV_FILE) -f $(COMPOSE_FILE) stop
	docker compose --env-file $(ENV_FILE) -f $(COMPOSE_FILE) up -d
.PHONY: stop
stop: ## stop containers
	docker compose --env-file $(ENV_FILE) -f $(COMPOSE_FILE) stop
.PHONY: down
down: ## bring down containers
	docker compose down
.PHONY: logs
logs: ## show logs of containers
	docker compose logs
.PHONY: ps
ps: ## show container status
	docker ps -a
.PHONY: destroy
destroy: ## destroy containers
	docker compose --env-file $(ENV_FILE) -f $(COMPOSE_FILE) down -v
.PHONY: test
test: ## run unit tests for auth microservice
	docker exec -e RUN_ENV=test backend-$(BUILD_ENV) pytest -v
.PHONY: testcov
testcov: ## run unit tests for auth microservice
	docker exec -e RUN_ENV=test backend-$(BUILD_ENV) pytest --cov

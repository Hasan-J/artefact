export COMPOSE_PROJECT_NAME := artefact_tests

DUMMY_FILE=.dummy

.PHONY: tests up down run clean

tests: $(DUMMY_FILE)
	@rm -f $(DUMMY_FILE)
	@make up run down

$(DUMMY_FILE):
	@touch $(DUMMY_FILE)

up: $(DUMMY_FILE)
	@docker compose up -d backend

run:
	docker compose run --rm backend pytest tests

down:
	@docker compose down

clean:
	@docker compose rm -f
	@rm -f $(DUMMY_FILE)

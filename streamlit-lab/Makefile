COMPOSE_BASE := docker compose

local-up:
	$(COMPOSE_BASE)	-f docker-compose-local.yml up -d;

local-down:
	$(COMPOSE_BASE)	-f docker-compose-local.yml down;

cloud-up:
	$(COMPOSE_BASE)	-f docker-compose-cloud.yml up -d;

cloud-down:
	$(COMPOSE_BASE)	-f docker-compose-cloud.yml down;

INTERFACE=interface_1
MACHINE=distsys_webserver_1
MONGO=mongo_1
REDIS=redis_1

default: build run

bash:
	docker exec -it $(MACHINE) /bin/bash

build:
	docker-compose build

down:
	docker-compose down

interface:
	docker exec -it $(MACHINE) python -m interface

mongo:
	docker exec -it $(MONGO) mongo

redis:
	docker exec -it $(REDIS) redis-cli

run:
	docker-compose up

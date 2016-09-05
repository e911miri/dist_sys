DIRNAME= distsys
INTERFACE=interface_1
MACHINE=distsys_webserver_1
MONGO=mongo_1
REDIS=redis_1

default: build up

build:
	docker-compose build

down:
	docker-compose down

up:
	docker-compose up

bash_rq:
	docker exec -it $(DIRNAME)_rq_1 /bin/bash

bash_webserver:
	docker exec -it $(DIRNAME)_webserver_1 /bin/bash

interface:
	docker exec -it $(DIRNAME)_webserver_1 python -m lib.app.interface

mongo:
	docker exec -it $(DIRNAME)_mongo_1 mongo

redis:
	docker exec -it $(DIRNAME)_redis_1 redis-cli


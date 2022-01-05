include .env.dev
export

app_name = ${FLASK_APP}

# --no-cache needs to be called if requirements.txt is updated
# otherwise it ignores new additions
build:
	docker build -t $(app_name) . --no-cache

server:
	docker-compose -f docker-compose-dev.yml up -d

kill:
	docker stop $(app_name) postgres
	docker container prune -f
	docker rmi -f $(app_name) postgres

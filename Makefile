include .env.dev
export

app_name = ${FLASK_APP}

build:
	docker build -t $(app_name) .

server:
	docker-compose -f docker-compose-dev.yml up -d

kill:
	docker stop $(app_name)
	docker container prune -f
	docker rmi -f $(app_name)

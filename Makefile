
app_name = ${FLASK_APP}

build:
	docker build -t $(app_name) .

run-dev:
	docker-compose -f docker-compose-dev.yml up --build

run-live:
	docker-compose -f docker-compose-live.yml up -d --build

kill:
	docker stop $(app_name)
	docker container prune -f
	docker rmi -f $(app_name)

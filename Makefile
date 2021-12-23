
app_name = silentlyfailing

build:
	docker build -t $(app_name) .

server:
	docker-compose -f docker-compose-dev.yml up --build

kill:
	docker stop $(app_name)
	docker container prune -f
	docker rmi -f $(app_name)

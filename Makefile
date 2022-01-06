app_name = silentlyfailing

# --no-cache needs to be called if requirements.txt is updated
# otherwise it ignores new additions
build:
	docker build -t $(app_name) . --no-cache

dev-server:
	docker-compose -f docker-compose-dev.yml up -d

live-server:
	flask db upgrade
	gunicorn "silentlyfailing:create_app()"

kill:
	docker stop $(app_name) postgres
	docker container prune -f
	docker rmi -f $(app_name) postgres

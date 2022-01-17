app_name = silentlyfailing

export FLASK_APP = $(app_name)

# --no-cache needs to be called if requirements.txt is updated
# otherwise it ignores new additions
build:
	docker build -t $(app_name) . --no-cache

# creates migrations, but needs the database to be created and running first
migrate:
	. venv/bin/activate
	flask db migrate

dev-server:
	docker-compose -f docker-compose-dev.yml up -d

live-server:
	flask db upgrade
	flask setup-admin
	gunicorn "silentlyfailing:create_app()"

kill:
	docker stop $(app_name) postgres
	docker container prune -f
	docker rmi -f $(app_name) postgres

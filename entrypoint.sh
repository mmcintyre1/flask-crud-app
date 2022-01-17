#!/usr/bin/env bash
# if starting manually, need to read in env var, uncomment following 2 lines
# export $(xargs <.env.dev)
# export POSTGRES_HOST=localhost
echo "Starting the application"
echo "Activating the virtual environment"
. venv/bin/activate
while true; do
    echo "Updating the database"
    flask db upgrade
    if [ $? -eq 0 ]; then
        break
    fi
    echo Deploy command failed, retrying in 5 secs...
    sleep 5
done
echo "Setting up admin user"
flask setup-admin
echo "Running flask server"
flask run --host=0.0.0.0

from flask.cli import FlaskGroup

from silentlyfailing import create_app


cli = FlaskGroup(create_app())


if __name__ == "__main__":
    cli()

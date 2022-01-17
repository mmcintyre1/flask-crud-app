import click
from flask import Blueprint


from silentlyfailing.models import setup_admin_user
from silentlyfailing import db


cmd = Blueprint('cmd', __name__)


@cmd.cli.command('setup-admin')
def setup_admin():
    """Create admin user."""
    setup_admin_user(db)
    click.echo("Admin user created.")

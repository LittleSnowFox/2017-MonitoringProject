# -*- coding: utf-8 -*-
import click
from flask.cli import FlaskGroup

"""
Contains features for the database administration
"""


# Import the application
def import_app(info):
    from run import app
    return app


# Generate a cli (Command Line Interface) group to add features to the manage.py
@click.group(cls=FlaskGroup, create_app=import_app)
def cli():
    pass


# Features
@cli.command()
def initdb():
    """
    Initialize the database
    """
    from server.run import db
    import server.users.models
    db.create_all()
    click.echo('Initialized the database')


@cli.command()
def dropdb():
    """
    Drop the database
    """
    from server.run import db
    import server.users.models
    db.drop_all()
    click.echo('Dropped the database')


if __name__ == '__main__':
    cli()

import os
from contextlib import suppress

import sqlalchemy
from app.database import db
from invoke import task, Collection

from app import create_app

db_collection = Collection('db')


def get_env(test=False):
    env = 'test' if test else 'development'
    os.environ['FLASK_CONFIGURATION'] = env
    return env


@task(help={'message': "Pass a message to the revision"})
def create(ctx, message, test=False):
    """ Invoke alembic to generate new migration from the existing db
        and service' models.
    """
    get_env(test)
    app = create_app()

    with app.app_context():
        import alembic.config
        alembic.config.main(argv=[
            '-c',
            'migrations/alembic.ini',
            'revision',
            '--autogenerate',
            '-m',
            message,
        ])


db_collection.add_task(create)


@task(help={'revision': "Pass the version you want to migrate to"})
def up(ctx, revision='head', test=False):
    """ Invoke alembic to migrate db up to current HEAD.
    """
    get_env(test)
    app = create_app()

    with app.app_context():
        import alembic.config
        alembic.config.main(argv=[
            '-c',
            'migrations/alembic.ini',
            'upgrade',
            revision,
        ])


db_collection.add_task(up)


@task
def down(ctx, revision='-1', test=False):
    """ Invoke alembic to migrate db down to base.
    """

    get_env(test)
    app = create_app()

    with app.app_context():
        import alembic.config
        alembic.config.main(argv=[
            '-c',
            'migrations/alembic.ini',
            'downgrade',
            revision
        ])


db_collection.add_task(down)


@task
def create(ctx, test=False):
    """ Create database defined in the config.
    """
    get_env(test)
    app = create_app()

    with app.app_context():
        # ignore error if database exist
        with suppress(sqlalchemy.exc.ProgrammingError):
            # make connection to database name: postgres
            with sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'], isolation_level='AUTOCOMMIT'
                                          ).connect() as connection:
                connection.execute(f"CREATE DATABASE postgres")


db_collection.add_task(create)


@task
def drop(ctx, test=False):
    """ Drop database defined in the config.
    """
    get_env(test)
    app = create_app()

    with app.app_context():
        # ignore error if database exist
        with suppress(sqlalchemy.exc.ProgrammingError):
            provider = app.config['DB'].provider

            # make connection to database name: postgres
            server_url = 'postgres://{user}:{pass}@{host}:{port}/postgres'.format(
                **app.config['DB'][provider])

            with sqlalchemy.create_engine(server_url, isolation_level='AUTOCOMMIT'
                                          ).connect() as connection:
                connection.execute(
                    f"DROP DATABASE IF EXISTS {app.config['DB'][provider].schema}")


db_collection.add_task(drop)


@task
def droptable(ctx, test=False):
    get_env(test)
    app = create_app()
    with app.app_context():
        db.drop_all(app=app)


db_collection.add_task(droptable)


@task
def createtable(ctx, test=False):
    get_env(test)
    app = create_app()
    with app.app_context():
        db.create_all(app=app)


db_collection.add_task(createtable)


@task
def truncate(ctx, test=False):
    """ Truncate data in all database tables and restart sequences
    """
    get_env(test)
    app = create_app()

    with app.app_context():
        db.engine.execute('TRUNCATE {} RESTART IDENTITY;'.format(
            ', '.join('public."{0}"'.format(table.name)
                      for table in reversed(db.metadata.sorted_tables))))


db_collection.add_task(truncate)


@task
def world(ctx, test=False):
    """ Down. Up. Populate.
    """
    down(ctx, test)
    up(ctx, test)


db_collection.add_task(world)

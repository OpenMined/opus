import os

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

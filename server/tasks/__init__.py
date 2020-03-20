from invoke import task, Collection

from .db import db_collection

ns = Collection()
ns.add_collection(db_collection)


@task
def list(ctx, release=False):
    """ List all available tasks
    """
    ctx.run('invoke --list')


ns.add_task(list)


@task
def vvv(ctx, release=False):
    """ Current service version
    """
    from service_ico import PACKAGE_VERSION
    print(PACKAGE_VERSION)


ns.add_task(vvv)


@task
def bump(ctx, bump):
    """ `inv bump <bumplevel>` Checkout master, execute a bump, push to origin.
    """
    assert bump in ('patch', 'minor', 'major')

    ctx.run('git checkout master')
    ctx.run('git pull')
    ctx.run('bumpversion {bump}'.format(bump=bump))
    ctx.run('git push')


ns.add_task(bump)

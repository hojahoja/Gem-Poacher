import platform

from coverage import coverage
from invoke import task


@task
def start(ctx):
    if platform.system() == 'Windows':
        ctx.run("python src/main.py")
    else:
        ctx.run("python src/main.py", pty=True)


@task
def test(ctx):
    if platform.system() == 'Windows':
        ctx.run("pytest src")
    else:
        ctx.run("pytest src", pty=True)


@task
def coverage(ctx):
    if platform.system() == 'Windows':
        ctx.run("coverage run --branch -m pytest src")
        ctx.run("coverage report -m")
    else:
        ctx.run("coverage run --branch -m pytest src", pty=True)
        ctx.run("coverage report -m")


@task(coverage)
def coverage_report(ctx):
    if platform.system() == 'Windows':
        ctx.run("coverage html")
    else:
        ctx.run("coverage html", pty=True)

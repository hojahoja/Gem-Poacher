import platform

from invoke import task


def platform_agnostic_command(ctx, command: str):
    if platform.system() == "Windows":
        ctx.run(command)
    else:
        command = command.replace("python", "python3")
        ctx.run(command, pty=True)


@task
def start(ctx):
    platform_agnostic_command(ctx, "python src/main.py")


@task
def test(ctx):
    platform_agnostic_command(ctx, "pytest src")


@task
def test_short(ctx):
    platform_agnostic_command(ctx, "pytest src --tb=short")


@task
def coverage(ctx):
    platform_agnostic_command(ctx, "coverage run --branch -m pytest src")
    platform_agnostic_command(ctx, "coverage report -m")


@task(coverage)
def coverage_report(ctx):
    platform_agnostic_command(ctx, "coverage html")


@task
def lint(ctx):
    platform_agnostic_command(ctx, "pylint src")


@task
def auto_format(ctx):
    platform_agnostic_command(ctx, "autopep8 --in-place --recursive src")

import os
import platform
from pathlib import Path

from invoke import task

PLATFORM = platform.system()


def platform_agnostic_command(ctx, command: str):
    if PLATFORM == "Windows":
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


@task
def create_config(ctx):
    platform_agnostic_command(ctx, "python src/generate_config.py")


@task
def create_database(ctx):
    platform_agnostic_command(ctx, "python src/initialize_database.py")


@task(create_database)
def build_binary(ctx):
    command = "pyinstaller --onedir --name gem-poacher --windowed"
    if PLATFORM == "Windows":
        command += " --icon=src/assets/icon/gem_poacher.ico"
    command += " --add-data=src/assets:assets"
    command += " --add-data=src/database/score.db:database"
    command += " --add-data=src/config/config.ini:config"
    command += " --contents-directory data"
    command += " src/main.py"
    platform_agnostic_command(ctx, command)

    _create_config_symlink(ctx)


def _create_config_symlink(ctx):
    cwd = Path(__file__).resolve().parent
    game_folder = cwd / "dist" / "gem-poacher"
    config_file = game_folder / "data" / "config" / "config.ini"
    config_link = game_folder / "config.ini"

    if not config_link.exists() and PLATFORM == "Linux":
        print("Creating config.ini symlink...")
        ctx.run(
            f"ln -s -r {str(config_file)} {str(game_folder / 'config.ini')}", pty=True
        )

    elif not config_link.with_suffix(".ini.lnk").exists() and PLATFORM == "Windows":
        print("Creating config.ini shortcut...")
        _create_windows_shortcut(ctx, cwd, game_folder, config_file, config_link)


def _create_windows_shortcut(ctx, cwd, game_folder, config_file, config_link):
    script_path = cwd / "create_shortcut.ps1"

    if not script_path.exists():
        script_content = f"""
        $WshShell = New-Object -comObject WScript.Shell
        $Shortcut = $WshShell.CreateShortcut("{config_link.with_suffix(".ini.lnk")}")
        $Shortcut.TargetPath = "{config_file}"
        $Shortcut.WorkingDirectory = "{game_folder}"
        $Shortcut.Save()
        """
        script_path.write_text(script_content.strip(), encoding="utf-8")

    ctx.run(f'powershell -ExecutionPolicy Bypass -File "{script_path}"')

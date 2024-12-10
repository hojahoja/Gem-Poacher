# Gem Poacher

A simple game where you move the mouse to collect gems while avoiding hostile
monsters on the screen. The idea is based on Jewel Thief.

A retro review of Jewel Thief by LazyGameReviews:

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/EIcImzLNMz8/0.jpg)](https://youtu.be/EIcImzLNMz8)

## Release

[GitHub release](https://github.com/hojahoja/Gem-Poacher/releases)

## Documentation

[Requirements Specification](documentation/requirements_specification.md) \
[Work Time Log](documentation/work_time_log.md) \
[Changelog](documentation/changelog.md) \
[Architecture](documentation/architecture.md) \
[User Manual](documentation/user_manual.md)

## Python Version

This game has been tested with Python version 3.12

## Command line

Run these commands inside powershell or preferred linux shell. \
[Poetry](https://python-poetry.org/docs/) has to be installed for these to work

### Install dependencies

```sh
poetry install
```

### Run the game

```sh
poetry run invoke start
```

### Testing

```sh
poetry run invoke test
```

### Check coverage

Get a coverage report inside the terminal with:

```sh
poetry run invoke coverage
```

### Coverage report

Generate a html report with:

```sh
poetry run invoke coverage-report
```

### Linter

Run pylint for the src folder with:

```sh
poetry run invoke lint
```

## Information about the original version

This game was originally my final submission for the
[Python programming mooc 2023](https://ohjelmointi-23.mooc.fi/osa-14/4-oma-peli).

My idea is to rewrite the game with a more sensible structure, documentation and
testing that will follow the guidelines and standards set by this course. I also
want to develop it further with more features than in the original.

[Code of the original version](documentation/misc/kolikkorosvo.py)


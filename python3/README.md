# My Utils

## Getting Started

### Install Poetry

```shell
# Linux, macOS, Windows
# https://python-poetry.org/docs/
curl -sSL https://install.python-poetry.org | python3 -

# Or with pipx
pipx install poetry
poetry version
```

### Run CLI commands

```shell
poetry install

# Call CLI tool with Python
poetry run python cm_util/main.py --help

# Call CLI tool with Poetry
poetry run cm-util --help

# Create project in editable mode (call from terminal as cm-util)
pip install -e .
```

### Run Tests

View run scripts in the `scripts.py` file.

```shell
poetry run test
poetry run coverage
```

#### Disclaimer

The youtube-dl and yt_dlp commands are for example only! Illegally downloading music is wrong and should never be done!

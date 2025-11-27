# My Utils

## Platform Requirements

**⚠️ macOS Only**: This CLI utility is specifically designed for macOS. It requires:
- macOS operating system (tested on Ventura and later)
- Chrome browser (optional, but recommended for some YouTube downloads)
- Apple Music app (for music file integration)

## Getting Started

### Install Poetry

```shell
# Linux, macOS, Windows
# https://python-poetry.org/docs/
curl -sSL https://install.python-poetry.org | python3 -

# Or with homebrew (macOS)
brew install poetry

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

```shell
# Run all unit tests (46 tests)
poetry run test

# Run tests with pytest directly
poetry run pytest cm_util/tests/

# Run specific test file
poetry run pytest cm_util/tests/unit/test_music.py

# Run with verbose output
poetry run pytest cm_util/tests/ -v
```

### Run Coverage

```shell
# Generate coverage report
poetry run coverage

# View coverage in terminal
poetry run coverage report -m

# Open HTML coverage report
open cm_util/htmlcov/index.html
```

Test scripts are defined in `scripts.py`.

## CLI Commands

### Download Song (YouTube/SoundCloud)
```shell
poetry run cm-util dl-song --url "https://youtube.com/watch?v=..."
poetry run cm-util dl-song --url "https://soundcloud.com/artist/track"
```

### Download Video (YouTube)
```shell
poetry run cm-util dl-video --url "https://youtube.com/watch?v=..."
```

### Download SoundCloud User Likes
```shell
poetry run cm-util dl-sc-user-likes --username "username"
```

### Open Applications
```shell
poetry run cm-util open-apps --type default
poetry run cm-util open-apps --type music
```

### Sort Files
```shell
poetry run cm-util order-files --path "/path/to/folder" --file-type mp3 --order-by date
```

## Disclaimer

The youtube-dl and yt_dlp commands are for educational purposes only! Illegally downloading copyrighted music is wrong and should never be done. Always respect copyright laws and content creators' rights.

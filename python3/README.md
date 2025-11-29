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
poetry run python mac_utils/main.py --help

# Call CLI tool with Poetry
poetry run mac-utils --help

# Create project in editable mode (call from terminal as mac-utils)
pip install -e .
```

## Testing

All commands must be run from the `python3` directory.

### Run Tests

```shell
# Navigate to python3 directory first
cd python3

# Install dependencies (required before first run)
poetry install

# Run all unit tests (46 tests)
poetry run test

# Run tests with pytest directly
poetry run pytest mac_utils/tests/

# Run specific test file
poetry run pytest mac_utils/tests/unit/test_music.py

# Run with verbose output
poetry run pytest mac_utils/tests/ -v
```

### Run Coverage

```shell
# Generate coverage report (from python3 directory)
poetry run coverage

# View coverage in terminal
poetry run coverage report -m

# Open HTML coverage report
open mac_utils/htmlcov/index.html
```

Test scripts are defined in `scripts.py`.

## CLI Commands

### Download Song (YouTube/SoundCloud)

```shell
poetry run mac-utils dl-song --url "https://youtube.com/watch?v=..."
poetry run mac-utils dl-song --url "https://soundcloud.com/artist/track"
```

### Download Video (YouTube)

```shell
poetry run mac-utils dl-video --url "https://youtube.com/watch?v=..."
```

### Download SoundCloud User Likes

```shell
poetry run mac-utils dl-sc-user-likes --username "username"
```

### Open Applications

```shell
poetry run mac-utils open-apps --type default
poetry run mac-utils open-apps --type music
```

### Sort Files

```shell
poetry run mac-utils order-files --path "/path/to/folder" --file-type mp3 --order-by date
```

## Disclaimer

The youtube-dl and yt_dlp commands are for educational purposes only! Illegally downloading copyrighted music is wrong and should never be done. Always respect copyright laws and content creators' rights.

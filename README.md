# My Personal CLI Utils

A collection of CLI commands that I use to help automate common tasks like downloading media from YouTube/SoundCloud, managing macOS applications, and organizing files.

## Platform Requirements

**⚠️ macOS Only**: This utility is designed for macOS and uses macOS-specific features:

- The `open` command for launching applications
- macOS file system paths (e.g., `/Applications`, `/System/Applications`)
- Apple Music integration via macOS-specific directories

**Prerequisites:**
- macOS (tested on Ventura and later)
- Python 3.11+
- Poetry (Python package manager)
- Chrome browser (optional, for authenticated downloads)

## Quick Start

### 1. Install Poetry

```bash
# Using the official installer
curl -sSL https://install.python-poetry.org | python3 -

# Or using pipx
pipx install poetry

# Verify installation
poetry --version
```

### 2. Install Dependencies

```bash
cd python3
poetry install
```

### 3. Run the CLI

```bash
# View available commands
poetry run cm-util --help

# Example: Download a song
poetry run cm-util dl-song --url "https://youtube.com/watch?v=..."

# Example: Download a video
poetry run cm-util dl-video --url "https://youtube.com/watch?v=..."
```

## Testing

### Run Tests

```bash
cd python3

# Run all tests
poetry run test

# Run tests with pytest directly
poetry run pytest cm_util/tests/

# Run specific test file
poetry run pytest cm_util/tests/unit/test_music.py

# Run with verbose output
poetry run pytest cm_util/tests/ -v
```

### Run Coverage

```bash
cd python3

# Generate coverage report
poetry run coverage

# View HTML coverage report
open cm_util/htmlcov/index.html
```

### Test Results

✅ **46 comprehensive tests** covering:
- Music downloads (YouTube, SoundCloud)
- Video downloads with file management
- URL validation
- Retry logic and error handling
- File operations

## Available Commands

- `open-apps` - Launch macOS applications
- `dl-song` - Download audio from YouTube/SoundCloud
- `dl-video` - Download video from YouTube
- `dl-sc-user-likes` - Download SoundCloud user's liked tracks
- `order-files` - Sort files by name, date, or size

Run `poetry run cm-util --help` for full command documentation.

## Development

### Project Structure

```
python3/
├── cm_util/          # Main package
│   ├── main.py       # CLI entry point
│   ├── util.py       # Core utilities
│   ├── music.py      # Music download logic
│   ├── video.py      # Video download logic
│   ├── config/       # Configuration files
│   └── tests/        # Test suite
├── scripts.py        # Test/coverage scripts
└── pyproject.toml    # Poetry configuration
```

### Key Features

- **Retry Logic**: Downloads retry 3 times with 2-second delays
- **URL Validation**: Comprehensive regex-based validation
- **Chrome Cookies**: Optional browser cookie support
- **Error Handling**: Graceful degradation when Chrome unavailable
- **Type Safety**: Type hints throughout codebase

## Generate Release Tag

```shell
npm run release
```

## Documentation

See `./python3/README.md` for detailed usage and `CLAUDE.md` for development guidance.

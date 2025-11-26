# My Personal CLI Utils

A collection of CLI commands that I use to help automate common tasks like downloading media from YouTube/SoundCloud, managing macOS applications, and organizing files.

## Platform Requirements

**⚠️ macOS Only**: This utility is designed for macOS and uses macOS-specific features:

- The `open` command for launching applications
- macOS file system paths (e.g., `/Applications`, `/System/Applications`)
- Apple Music integration via macOS-specific directories

**Prerequisites:**
- macOS (tested on Ventura and later)
- Python 3.13+
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

## Global Installation (Run from Anywhere)

To use `cm-util` commands from any terminal without needing to be in the project directory:

### Option 1: Using pipx (Recommended)

This installs the CLI tool globally while keeping it isolated:

```bash
# Install pipx if you don't have it
brew install pipx
pipx ensurepath

# Install cm-util globally
cd /Users/coopermiller/Development/GitHub/personal-utils/python3
pipx install .

# Now you can run from anywhere
cm-util dl-song --url "https://youtube.com/..."
```

To update after making changes:
```bash
cd /Users/coopermiller/Development/GitHub/personal-utils/python3
pipx reinstall cm-util
```

### Option 2: Add Poetry virtualenv to PATH

Add the Poetry virtualenv's bin directory to your shell PATH:

```bash
# Find your virtualenv path
cd /Users/coopermiller/Development/GitHub/personal-utils/python3
poetry env info --path

# Add to your ~/.zshrc or ~/.bashrc:
export PATH="$(poetry env info --path)/bin:$PATH"

# Reload your shell config
source ~/.zshrc  # or source ~/.bashrc

# Now you can run from anywhere
cm-util dl-song --url "https://youtube.com/..."
```

### Option 3: Shell Alias

Add an alias to your shell config (`~/.zshrc` or `~/.bashrc`):

```bash
# Add this line to ~/.zshrc
alias cm-util='poetry -C /Users/coopermiller/Development/GitHub/personal-utils/python3 run cm-util'

# Reload your shell
source ~/.zshrc

# Now you can run from anywhere
cm-util dl-song --url "https://youtube.com/..."
```

### Verify Installation

Test that it works from any directory:

```bash
# Navigate to a different directory
cd ~

# Run a command
cm-util --help
cm-util --version
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

### Media Downloads
- `dl-song` - Download audio from YouTube/SoundCloud as MP3
- `dl-video` - Download video from YouTube
- `dl-sc-user-likes` - Download all tracks a SoundCloud user has liked

### System & File Management
- `open-apps` - Launch macOS applications (system, installed, or music apps)
- `order-files` - Sort files in a directory by name, date, or size

### Configuration & History
- `config` - View and manage configuration settings
- `history` - View download history and manage duplicates

### Global Options
- `--verbose`, `-v` - Enable verbose output (DEBUG level)
- `--quiet`, `-q` - Suppress output except errors
- `--dry-run` - Preview what would be downloaded without downloading
- `--output-dir`, `-o` - Specify custom output directory
- `--force`, `-f` - Force download even if URL exists in history
- `--version` - Show version information

Run `cm-util --help` or `cm-util [command] --help` for detailed documentation.

### Usage Examples

```bash
# Download a song from YouTube
cm-util dl-song --url "https://youtube.com/watch?v=dQw4w9WgXcQ"

# Download with custom output directory
cm-util --output-dir ~/Music/NewSongs dl-song --url "https://youtube.com/..."

# Download a video (verbose mode)
cm-util --verbose dl-video --url "https://youtube.com/watch?v=..."

# Preview without downloading (dry run)
cm-util --dry-run dl-song --url "https://youtube.com/..."

# Force re-download even if already in history
cm-util --force dl-song --url "https://youtube.com/..."

# View download history
cm-util history --limit 20

# View and edit configuration
cm-util config
cm-util config --set output_dir --value ~/Downloads/Music

# Download SoundCloud user's liked tracks
cm-util dl-sc-user-likes --username "your-username"

# Sort files in a directory
cm-util order-files --path ~/Downloads --file-type mp3 --order-by date
```

## Development

### Project Structure

```md
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

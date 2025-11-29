# mac-utils

A collection of macOS CLI utilities to automate common tasks like downloading media from YouTube/SoundCloud, managing applications, and organizing files.

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

# Or using homebrew (macOS)
brew install poetry

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
poetry run mac-utils --help

# Example: Download a song (simple!)
poetry run mac-utils dl-song "https://youtube.com/watch?v=..."

# Example: Download a video
poetry run mac-utils dl-video "https://youtube.com/watch?v=..."
```

## Global Installation (Run from Anywhere)

Choose one of these options to use `mac-utils` from any terminal without being in the project directory:

| Method                   | Best For       | Updates After Code Changes   | Setup Complexity |
| ------------------------ | -------------- | ---------------------------- | ---------------- |
| **pipx**                 | Production use | Need to run `pipx reinstall` | Easy             |
| **Shell Alias** (Poetry) | Development    | Automatic ✨                 | Very Easy        |
| **PATH Export**          | Power users    | Automatic                    | Medium           |

**Quick Recommendation:**

- **Developing?** Use Option 2 (Shell Alias with Poetry)
- **Just using the tool?** Use Option 1 (pipx)

### Option 1: Using pipx (Recommended for Production Use)

**Best for:** Installing as a standalone global tool that auto-updates with git pulls.

pipx installs the CLI tool globally while keeping dependencies isolated:

```bash
# 1. Install pipx if you don't have it
brew install pipx
pipx ensurepath

# 2. Navigate to the python3 directory
cd ./personal-utils/python3

# 3. Install mac-utils globally
pipx install .

# 4. Now you can run from anywhere!
cd ~
mac-utils dl-song "https://youtube.com/watch?v=..."
mac-utils --version
```

**After making code changes:**

```bash
cd ./personal-utils/python3
pipx reinstall mac-utils
```

---

### Option 2: Shell Alias with Poetry (Recommended for Development)

**Best for:** Active development - no reinstall needed after code changes.

Add an alias to your shell config file:

#### For zsh (macOS default):

```bash
# Open your zsh config file
vi ~/.zshrc

# Add this line at the end (replace with your actual path):
alias mac-utils='poetry -C ./personal-utils/python3 run mac-utils'

# Save and exit (Esc, :wq, Enter)

# Reload your shell config
source ~/.zshrc
```

#### For bash:

```bash
# Open your bash config file
vi ~/.bashrc

# Add this line at the end (replace with your actual path):
alias mac-utils='poetry -C ./python3 run mac-utils'

# Save and exit (Esc, :wq, Enter)

# Reload your shell config
source ~/.bashrc
```

**Now you can run from anywhere:**

```bash
cd ~
mac-utils dl-song "https://youtube.com/watch?v=..."
mac-utils --help
```

**Benefits:**

- No reinstall needed after code changes
- Always uses latest code from your repo
- Perfect for active development

---

### Option 3: Add Poetry virtualenv to PATH

**Best for:** Direct access to all Poetry-installed scripts.

```bash
# 1. Navigate to the python3 directory
cd ./python3

# 2. Get the virtualenv path
poetry env info --path
# Example output: /Users/coopermiller/Library/Caches/pypoetry/virtualenvs/mac-utils-xxxxx-py3.13

# 3. Add to your shell config (~/.zshrc or ~/.bashrc)
echo 'export PATH="/Users/coopermiller/Library/Caches/pypoetry/virtualenvs/mac-utils-xxxxx-py3.13/bin:$PATH"' >> ~/.zshrc

# 4. Reload your shell
source ~/.zshrc

# 5. Now you can run from anywhere
mac-utils dl-song "https://youtube.com/..."
```

**Note:** You'll need to update the PATH if you recreate the virtualenv.

---

### Bonus: Create Shorter Command Aliases

After setting up global installation (any option above), you can create convenient short aliases for frequently used commands:

#### For zsh (macOS default):

```bash
# Open your zsh config file
vi ~/.zshrc

# Add these convenient aliases at the end:
alias mudls='mac-utils dl-song'           # Download song
alias mudlv='mac-utils dl-video'          # Download video

# Save and exit (Esc, :wq, Enter)

# Reload your shell config
source ~/.zshrc
```

#### For bash:

```bash
# Open your bash config file
vi ~/.bashrc

# Add these convenient aliases at the end:
alias mudls='mac-utils dl-song'           # Download song
alias mudlv='mac-utils dl-video'          # Download video
alias mudlsc='mac-utils dl-sc-user-likes' # Download SoundCloud likes
alias muconfig='mac-utils config'         # Manage config
alias muhistory='mac-utils history'       # View history

# Save and exit (Esc, :wq, Enter)

# Reload your shell config
source ~/.bashrc
```

**Now you can use super short commands:**

```bash
# Download a song with just 5 characters!
mudls "https://youtube.com/watch?v=dQw4w9WgXcQ"

# Download a video
mudlv "https://youtube.com/watch?v=..."

# Download SoundCloud user likes
mudlsc username

# Check config
muconfig --show

# View download history
muhistory --show --limit 10
```

**Customize your own aliases:**
Feel free to create your own short aliases! Common patterns:

- `mu` = mac-utils (prefix)
- `dls` = download song
- `dlv` = download video
- Or use whatever makes sense to you!

---

### Verify Installation

Test that it works from any directory:

```bash
# Navigate to a different directory
cd ~

# Run a command
mac-utils --help
mac-utils --version
```

## Testing

### Run Tests

```bash
cd python3

# Run all tests
poetry run test

# Run tests with pytest directly
poetry run pytest mac_utils/tests/

# Run specific test file
poetry run pytest mac_utils/tests/unit/test_music.py

# Run with verbose output
poetry run pytest mac_utils/tests/ -v
```

### Run Coverage

```bash
cd python3

# Generate coverage report
poetry run coverage

# View HTML coverage report
open mac_utils/htmlcov/index.html
```

### Test Results

✅ **46 comprehensive tests** covering:

- Music downloads (YouTube, SoundCloud)
- Video downloads with file management
- URL validation
- Retry logic and error handling``
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

Run `mac-utils --help` or `mac-utils [command] --help` for detailed documentation.

### Usage Examples

**Using full commands:**

```bash
# Download a song from YouTube (simple positional argument!)
mac-utils dl-song "https://youtube.com/watch?v=dQw4w9WgXcQ"

# Download with custom output directory
mac-utils --output-dir ~/Music/NewSongs dl-song "https://youtube.com/..."

# Download a video (verbose mode)
mac-utils --verbose dl-video "https://youtube.com/watch?v=..."

# Preview without downloading (dry run)
mac-utils --dry-run dl-song "https://youtube.com/..."

# Force re-download even if already in history
mac-utils --force dl-song "https://youtube.com/..."

# View download history
mac-utils history --limit 20

# View and edit configuration
mac-utils config
mac-utils config --set output_dir --value ~/Downloads/Music

# Download SoundCloud user's liked tracks (positional argument!)
mac-utils dl-sc-user-likes username

# Sort files in a directory
mac-utils order-files --path ~/Downloads --file-type mp3 --order-by date
```

**Using short aliases** (if you set them up in the Bonus section above):

```bash
# Download a song - super quick! ⚡
mudls "https://youtube.com/watch?v=dQw4w9WgXcQ"

# Download a video
mudlv "https://youtube.com/watch?v=..."

# With global options (still works!)
mac-utils --verbose mudls "https://youtube.com/..."
mac-utils --dry-run mudlv "https://youtube.com/..."

# Download SoundCloud user likes
mudlsc username

# Check history
muhistory --show --limit 10

# Update config
muconfig --set output_dir --value ~/Music
```

## Development

### Linting and Code Quality

Run linting checks locally (same as GitHub Actions CI):

```bash
cd python3

# Check all linting (recommended before committing)
./lint.sh

# Auto-fix formatting issues
./lint-fix.sh

# Or run individual checks:
poetry run black --check .          # Check formatting
poetry run black .                  # Auto-fix formatting
poetry run isort --check-only .     # Check import sorting
poetry run isort .                  # Auto-fix import sorting
poetry run flake8 mac_utils/
poetry run mypy mac_utils/
```

### Project Structure

```md
python3/
├── mac_utils/ # Main package
│ ├── main.py # CLI entry point
│ ├── util.py # Core utilities
│ ├── music.py # Music download logic
│ ├── video.py # Video download logic
│ ├── config/ # Configuration files
│ └── tests/ # Test suite
├── scripts.py # Test/coverage scripts
└── pyproject.toml # Poetry configuration
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

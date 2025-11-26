# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a personal CLI utility toolkit (`cm-util`) built with Python and Poetry. The primary purpose is to automate common tasks like downloading media from YouTube/SoundCloud, managing macOS applications, and organizing files.

## Development Setup

### Python/Poetry Setup
```bash
# Install dependencies
cd python3
poetry install

# Run CLI (two methods)
poetry run python cm_util/main.py --help
poetry run cm-util --help

# Install in editable mode for system-wide access
pip install -e .
```

### Running Tests
```bash
cd python3
poetry run test          # Run unit tests
poetry run coverage      # Run coverage report
```

Tests are located in `python3/cm_util/tests/unit/`. The test runner is defined in `python3/scripts.py`.

### Version Management
```bash
# At project root
npm run release  # Creates version tag using standard-version and pushes to main
```

The project uses husky for git hooks and commitlint for conventional commits.

## Architecture

### CLI Structure
The CLI is built with Typer and organized as follows:

- **main.py**: Entry point with Typer commands (`open_apps`, `dl_song`, `dl_video`, `dl_sc_user_likes`, `order_files`)
- **util.py**: Core utilities shared across commands
  - yt-dlp wrapper functions (`yt_dlp_download`, `get_yt_dl_options`)
  - File operations (`sort_files_by`, `move_mp3_files_to_music_folder`)
  - macOS app launching (`open_apps`, `open_app`)
  - System path detection (`get_comp_user_name`, `get_itunes_music_folder`)
- **music.py**: Music download orchestration (downloads + moves to Apple Music)
- **video.py**: Video download functionality

### Key Design Patterns

1. **Media Downloads**: All media downloads use yt-dlp through `util.yt_dlp_download()`. This function:
   - Takes URL, media company (YouTube/SoundCloud), and media type (mp3/video)
   - Uses `get_yt_dl_options()` to configure format and postprocessing
   - Handles Chrome cookie extraction for authentication

2. **Apple Music Integration**: MP3 files are automatically moved to the macOS Music app's auto-import folder at:
   `/Users/{username}/Music/Music/Media.localized/Automatically Add to Music.localized`

3. **App Configuration**: Application lists are stored in `python3/cm_util/config/my-apps.json` with structure:
   ```json
   {
     "installed": {"path": "...", "apps": [...]},
     "system": {"path": "...", "apps": [...]},
     "music": {"path": "...", "apps": [...]}
   }
   ```

### Important Implementation Details

- The project assumes macOS (uses `system("open ...")` and macOS-specific paths)
- URL cleaning in `util.clean_url()` handles backslash escaping from terminal copy/paste
- Chrome browser cookies are required for certain YouTube downloads
- MP3 files are processed with FFmpeg for audio extraction (192kbps, 44.1kHz, stereo)

## Working with This Codebase

### Adding New CLI Commands
1. Add command function in `main.py` using `@app.command()` decorator
2. Implement core logic in appropriate module (`util.py`, `music.py`, `video.py`)
3. Follow existing pattern: logging, error handling, Typer options

### Modifying Download Behavior
- Edit `get_yt_dl_options()` in `util.py` to change yt-dlp configuration
- yt-dlp CLI reference: Lines 33-34 in `util.py` show equivalent CLI command

### Testing
- Unit tests use pytest
- Test files are in `cm_util/tests/files/` (e.g., test MP3s)
- Coverage config omits tests and `__init__.py` files (see `pyproject.toml`)

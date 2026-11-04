# Bloomplay

A lightweight terminal-based video player built with Python and VLC.

Bloomplay is a simple video player designed to organize and play local video collections through a terminal interface. It supports playlists, multiple playback modes, playback history, and customizable settings.

**Version:** 1.0.0  
**Status:** Initial Release  
**Project:** Chroma Flower

## Features

- Random, sequential, and repeat playback modes.
- Automatic video library scanning.
- Recursive folder scanning.
- Automatic playlist organization based on folders.
- Search videos by filename.
- Select playlists through the terminal.
- Refresh the video library without restarting.
- Playback history.
- Replay previously watched videos.
- Configurable volume and fullscreen mode.
- Option to resume the last played video.
- Keyboard shortcuts.
- Error logging.

## Requirements

- Python 3.10 or newer.
- VLC Media Player.
- Python dependencies listed in `requirements.txt`.

## Installation

### 1. Install VLC

Download and install VLC Media Player:

https://www.videolan.org/vlc/

### 2. Install Python

Download Python:

https://www.python.org/downloads/

Make sure Python is available in your system PATH.

### 3. Install dependencies

Open a terminal in the Bloomplay project directory and run:

```bash
python -m pip install -r requirements.txt
```

## Configuration

Before running Bloomplay, you need to configure the location of your video library.

### 1. Open config.json

Find the `config.json` file in the root directory of the project.

```text
Bloomplay/
├── bloomplay.py
├── config.json  <-- Edit this file
├── requirements.txt
└── src/
```

### 2. Set your video folder

Open `config.json` and find the following line:

```json
"video_folder": "CHANGE_THIS_TO_YOUR_VIDEO_FOLDER"
```

Replace the placeholder with the full path to your video directory.

**Windows example:**

```json
"video_folder": "D:\\Videos\\Bloomplay"
```

**Linux example:**

```json
"video_folder": "/home/user/Videos/Bloomplay"
```

**macOS example:**

```json
"video_folder": "/Users/user/Movies/Bloomplay"
```

Save the file before launching Bloomplay.

### Configuration options

The `config.json` file also controls other application settings.

| Setting | Description |
|---|---|
| `video_folder` | Location of the video library. |
| `fullscreen` | Enables fullscreen playback. |
| `volume` | Default volume (0–100). |
| `history_limit` | Maximum number of history entries. |
| `playback_mode` | Default playback mode. |
| `resume_last_video` | Resumes the last available video on startup. |

Available playback modes:

- `shuffle`
- `sequential`
- `repeat`

## Running Bloomplay

After installing the dependencies and configuring your video folder, open a terminal in the project directory and execute:

```bash
python bloomplay.py
```

## Video Library

Bloomplay scans the configured video directory recursively.

The first-level subfolders are automatically recognized as playlists. Videos directly inside the main directory belong to the `General` playlist.

Example:

```text
Videos/
├── video1.mp4
├── video2.mp4
├── Music/
│   ├── music1.mp4
│   └── music2.mp4
├── Gameplay/
│   ├── gameplay1.mp4
│   └── gameplay2.mp4
└── Movies/
    ├── movie1.mp4
    └── movie2.mp4
```

### Supported formats

- MP4
- MKV
- AVI
- MOV
- WMV
- WEBM
- FLV
- M4V
- MPEG
- MPG

## Keyboard Shortcuts

| Key | Action |
|---|---|
| Space | Pause / Resume |
| N | Next video |
| B | Previous video |
| M | Mute / Unmute |
| F | Toggle fullscreen |
| H | Open playback history |
| L | Search videos |
| S | Select playlist |
| R | Refresh library |
| C | Clear history |
| 1 | Shuffle mode |
| 2 | Sequential mode |
| 3 | Repeat mode |
| Up / Down | Adjust volume |
| Q | Quit Bloomplay |

## Project Structure

```text
Bloomplay/
├── bloomplay.py
├── config.json
├── requirements.txt
├── README.md
├── LICENSE
├── CHANGELOG.md
├── src/
│   └── bloomplay/
│       ├── __init__.py
│       ├── app.py
│       ├── player.py
│       ├── library.py
│       ├── history.py
│       ├── config.py
│       └── controls.py
└── tests/
    ├── test_library.py
    └── test_history.py
```

## Data and Logs

Bloomplay stores application data separately from the source code.

Default location:

```text
~/.bloomplay/
├── history.json
└── bloomplay.log
```

- `history.json`: Stores playback history.
- `bloomplay.log`: Stores application logs.

The main configuration file, `config.json`, remains in the project root.

## Compatibility

Bloomplay is designed for:

- Windows
- Linux
- macOS

Keyboard shortcut behavior may vary depending on the operating system and desktop environment.

On Linux, global keyboard shortcuts may be restricted under Wayland. On macOS, additional accessibility permissions may be required.

Compatibility across all listed systems has not been confirmed unless individually tested.

## Tests

Run the automated tests from the project root:

```bash
python -m unittest discover -s tests
```

## License

Bloomplay uses a custom license.

The project may be used, modified, and redistributed free of charge. Selling the original project or modified versions is prohibited. Derivative works must remain open source and follow the same license.

See [LICENSE](LICENSE) for the complete terms.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and changes.

---

**Bloomplay**  
*Part of the Chroma Flower creative ecosystem.*

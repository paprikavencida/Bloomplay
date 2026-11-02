# Bloomplay

**Random Video Player**

Bloomplay is a lightweight Python-based video player that automatically plays videos from a selected directory in random order.

It detects playlists, combines videos from multiple folders and provides continuous playback with simple terminal-based controls.

## Features

- Random video playback.
- Automatic playback when a video finishes.
- Continuous playback (infinite loop).
- Automatic playlist detection.
- Support for multiple playlists and nested folders.
- Combines videos from all playlists into a single random playback queue.
- Prevents the same video from playing twice in a row.
- Playback history with previous video navigation.
- Pause and resume controls.
- Skip to the next random video.
- Lightweight playback powered by VLC.

## Requirements

Before using Bloomplay, make sure you have:

- Python 3.8 or newer.
- VLC Media Player installed on your computer.
- Python-VLC library.

## Installation

### 1. Install VLC Media Player

Download and install VLC from the official website:

https://www.videolan.org/vlc/

### 2. Install Python dependencies

Open your terminal and run:

```bash
pip install python-vlc
```

### 3. Download the project

Clone the repository:

```bash
git clone YOUR_REPOSITORY_URL
```

Or download the repository as a ZIP file and extract it.

## Configuration

Open `random_player.py` and locate the following line:

```python
VIDEO_FOLDER = r"C:\Users\YourUser\Videos"
```

Replace the path with the directory containing your playlists.

Example:

```python
VIDEO_FOLDER = r"D:\Media\Videos"
```

### Supported formats

- MP4
- MKV
- AVI
- MOV
- WMV
- WEBM
- FLV

## Folder Structure

Bloomplay automatically detects playlists inside the main video directory. Each subfolder is treated as a playlist.

```text
Bloomplay/
│
├── random_player.py
│
└── Videos/
    │
    ├── Ambient/
    │   ├── video1.mp4
    │   └── video2.mp4
    │
    ├── Gameplay/
    │   ├── video1.mp4
    │   └── video2.mp4
    │
    ├── Music/
    │   ├── video1.mp4
    │   └── video2.mp4
    │
    └── Random/
        ├── video1.mp4
        └── video2.mp4
```

All videos from every detected playlist are combined into a single random playback queue.

You don't need to select a playlist manually. Bloomplay also supports nested folders inside playlists.

## Usage

After configuring the video directory, open a terminal in the project folder and execute:

```bash
python random_player.py
```

Bloomplay will automatically:

1. Scan all playlists and nested folders.
2. Collect supported video files.
3. Select a random video.
4. Start playback.
5. Wait until the video finishes.
6. Select another random video.
7. Repeat the process indefinitely.

## Playback Controls

Bloomplay provides simple terminal-based playback controls.

| Command | Action |
|---|---|
| `P` | Pause / Resume playback |
| `N` | Skip to the next random video |
| `B` | Return to the previous video |
| `Q` | Quit Bloomplay |

**Note:** Commands must be entered in the terminal followed by `Enter`.

## Technologies

- Python
- VLC Media Player
- python-vlc

## Future Improvements

- Manual playlist selection.
- Fullscreen playback.
- Volume controls.
- Graphical user interface.
- Custom playback modes.
- Persistent playback history.
- Configuration file (`config.json`).
- Automatic startup.

## License

This project is open-source. A license can be added when the project's distribution terms are defined.

---

**Bloomplay**  
*Part of the Chroma Flower creative ecosystem.*

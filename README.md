# Bloomplay

**Random Video Player**

Bloomplay is a simple Python-based video player that automatically plays videos from a selected folder in random order.

The player automatically selects another video whenever the current one finishes, creating a continuous playback experience without requiring manual interaction.

## Features

- Random video selection.
- Automatic playback of the next video.
- Continuous playback (infinite loop).
- Prevents the same video from playing twice in a row.
- Supports multiple video formats.
- Lightweight Python script.

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

Replace the path with the folder containing your videos.

Example:

```python
VIDEO_FOLDER = r"D:\Media\Videos"
```

Bloomplay automatically detects supported video files inside the selected folder.

### Supported formats

- MP4
- MKV
- AVI
- MOV
- WMV
- WEBM
- FLV

## Usage

After configuring the video folder, open a terminal in the project directory and execute:

```bash
python random_player.py
```

Bloomplay will automatically:

1. Scan the selected folder for videos.
2. Select a random video.
3. Start playback.
4. Wait until the video finishes.
5. Select another random video.
6. Repeat the process indefinitely.

To stop playback, press `Ctrl + C` in the terminal.

## Project Structure

```text
Bloomplay/
│
├── random_player.py
└── README.md
```

## Future Improvements

Possible features for future versions:

- Fullscreen playback.
- Graphical user interface.
- Playback controls (Play, Pause and Next).
- Custom playlists.
- Automatic startup.

## Technologies

- Python
- VLC Media Player
- python-vlc

## License

This project is open-source. A license can be added when the project's distribution terms are defined.

---

**Bloomplay**  
*Developed as part of Chroma Flower — Creative Technology & Media.*

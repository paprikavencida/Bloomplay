from pathlib import Path

VIDEO_EXTENSIONS = {
    ".mp4", ".mkv", ".avi", ".mov", ".wmv",
    ".webm", ".flv", ".m4v", ".mpeg", ".mpg"
}

def scan_videos(folder):
    root = Path(folder).expanduser()
    if not root.is_dir():
        return []

    library = []
    try:
        paths = root.rglob("*")
        for path in paths:
            try:
                if not path.is_file() or path.suffix.lower() not in VIDEO_EXTENSIONS:
                    continue
                relative = path.relative_to(root)
                playlist = relative.parts[0] if len(relative.parts) > 1 else "General"
                library.append({"path": path.resolve(), "playlist": playlist})
            except (OSError, ValueError):
                continue
    except OSError:
        return []

    return sorted(library, key=lambda item: str(item["path"]).casefold())

def playlists(videos):
    return sorted({video["playlist"] for video in videos}, key=str.casefold)

def search_videos(videos, query):
    query = query.casefold().strip()
    return [video for video in videos if query in video["path"].name.casefold()]

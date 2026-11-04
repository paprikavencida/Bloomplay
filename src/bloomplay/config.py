import json
import platform
from pathlib import Path

APP_DIR = Path.home() / ".bloomplay"

PROJECT_DIR = Path(__file__).resolve().parents[2]

CONFIG_FILE = PROJECT_DIR / "config.json"
HISTORY_FILE = APP_DIR / "history.json"
LOG_FILE = APP_DIR / "bloomplay.log"

DEFAULT_CONFIG = {
    "video_folder": str(
        Path.home() / (
            "Movies" if platform.system() == "Darwin" else "Videos"
        )
    ),
    "fullscreen": True,
    "volume": 70,
    "history_limit": 100,
    "playback_mode": "shuffle",
    "resume_last_video": False
}


def _atomic_write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)

    temp = path.with_suffix(path.suffix + ".tmp")

    with temp.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    temp.replace(path)


def load_config():
    APP_DIR.mkdir(parents=True, exist_ok=True)

    config = DEFAULT_CONFIG.copy()

    if not CONFIG_FILE.exists():
        save_config(config)

    else:
        try:
            saved = json.loads(
                CONFIG_FILE.read_text(encoding="utf-8")
            )

            if isinstance(saved, dict):
                config.update(saved)

        except (OSError, json.JSONDecodeError):
            print("Error: Could not read config.json.")
            print(f"Config location: {CONFIG_FILE}")
            raise

    try:
        config["volume"] = max(
            0, min(100, int(config["volume"]))
        )
    except (TypeError, ValueError):
        config["volume"] = DEFAULT_CONFIG["volume"]

    try:
        config["history_limit"] = max(
            1, int(config["history_limit"])
        )
    except (TypeError, ValueError):
        config["history_limit"] = DEFAULT_CONFIG["history_limit"]

    if config.get("playback_mode") not in {
        "shuffle",
        "sequential",
        "repeat"
    }:
        config["playback_mode"] = "shuffle"

    config["fullscreen"] = bool(config["fullscreen"])
    config["resume_last_video"] = bool(
        config["resume_last_video"]
    )

    folder = config.get("video_folder")

    if not isinstance(folder, str) or not folder.strip():
        raise ValueError("Invalid video_folder in config.json.")

    video_folder = Path(folder).expanduser()

    if not video_folder.is_absolute():
        video_folder = PROJECT_DIR / video_folder

    config["video_folder"] = str(video_folder.resolve())

    if not video_folder.exists():
        print("Warning: Video folder does not exist:")
        print(config["video_folder"])

    elif not video_folder.is_dir():
        print("Warning: The configured path is not a directory:")
        print(config["video_folder"])

    save_config(config)

    return config


def save_config(config):
    _atomic_write(CONFIG_FILE, config)
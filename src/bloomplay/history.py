import json
from datetime import datetime
from pathlib import Path
from .config import HISTORY_FILE

class PlaybackHistory:
    def __init__(self, limit=100, path=HISTORY_FILE):
        self.limit = limit
        self.path = Path(path)
        self.items = self._load()

    def _load(self):
        if not self.path.exists():
            return []
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            if isinstance(data, list):
                return [item for item in data if isinstance(item, dict) and isinstance(item.get("path"), str)]
        except (OSError, json.JSONDecodeError):
            print("Warning: history file is invalid; starting a new history.")
        return []

    def _save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temp = self.path.with_suffix(self.path.suffix + ".tmp")
        temp.write_text(json.dumps(self.items[:self.limit], indent=4, ensure_ascii=False), encoding="utf-8")
        temp.replace(self.path)

    def add(self, video):
        self.items.insert(0, {
            "path": str(video["path"]),
            "playlist": video["playlist"],
            "played_at": datetime.now().astimezone().isoformat(timespec="seconds")
        })
        self.items = self.items[:self.limit]
        self._save()

    def clear(self):
        self.items = []
        self._save()

    def existing_items(self):
        return [item for item in self.items if Path(item["path"]).is_file()]

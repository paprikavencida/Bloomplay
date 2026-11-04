import tempfile
import unittest
from pathlib import Path
from src.bloomplay.history import PlaybackHistory

class HistoryTests(unittest.TestCase):
    def test_add_and_limit(self):
        with tempfile.TemporaryDirectory() as folder:
            history = PlaybackHistory(limit=2, path=Path(folder) / "history.json")
            history.add({"path": "/tmp/a.mp4", "playlist": "A"})
            history.add({"path": "/tmp/b.mp4", "playlist": "B"})
            history.add({"path": "/tmp/c.mp4", "playlist": "C"})
            self.assertEqual(len(history.items), 2)
            self.assertEqual(Path(history.items[0]["path"]).name, "c.mp4")

    def test_clear(self):
        with tempfile.TemporaryDirectory() as folder:
            history = PlaybackHistory(limit=5, path=Path(folder) / "history.json")
            history.add({"path": "/tmp/a.mp4", "playlist": "A"})
            history.clear()
            self.assertEqual(history.items, [])

if __name__ == "__main__":
    unittest.main()

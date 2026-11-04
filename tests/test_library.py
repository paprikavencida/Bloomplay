import tempfile
import unittest
from pathlib import Path
from src.bloomplay.library import scan_videos, playlists, search_videos

class LibraryTests(unittest.TestCase):
    def test_recursive_scan_and_root_files(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "video.mp4").touch()
            (root / "Ambient" / "Nested").mkdir(parents=True)
            (root / "Ambient" / "Nested" / "song.mkv").touch()
            (root / "Ambient" / "notes.txt").touch()

            videos = scan_videos(root)
            self.assertEqual(len(videos), 2)
            self.assertEqual({v["playlist"] for v in videos}, {"General", "Ambient"})

    def test_search_and_playlists(self):
        videos = [
            {"path": Path("/tmp/clip-one.mp4"), "playlist": "Games"},
            {"path": Path("/tmp/music.mkv"), "playlist": "Music"}
        ]
        self.assertEqual(len(search_videos(videos, "CLIP")), 1)
        self.assertEqual(playlists(videos), ["Games", "Music"])

if __name__ == "__main__":
    unittest.main()

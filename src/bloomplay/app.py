import logging
import random
import time
from pathlib import Path
from queue import Empty, Queue

from .config import load_config, save_config
from .controls import start_listener
from .history import PlaybackHistory
from .library import scan_videos, playlists, search_videos
from .player import VideoPlayer

def setup_logging(log_path):
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s"
    )

class Bloomplay:
    def __init__(self):
        self.config = load_config()
        self.video_folder = Path(self.config["video_folder"]).expanduser()
        self.history = PlaybackHistory(self.config["history_limit"])
        self.queue = Queue()
        self.library = scan_videos(self.video_folder)
        self.filtered_library = self.library[:]
        self.session = []
        self.session_index = -1
        self.mode = self.config["playback_mode"]
        self.listener = None
        setup_logging(__import__("pathlib").Path.home() / ".bloomplay" / "bloomplay.log")
        self.player = VideoPlayer(
            volume=self.config["volume"],
            fullscreen=self.config["fullscreen"],
            event_queue=self.queue
        )
        self.running = True

    def save_settings(self):
        self.config["volume"] = self.player.volume
        self.config["fullscreen"] = self.player.fullscreen
        self.config["playback_mode"] = self.mode
        save_config(self.config)

    def print_help(self):
        print("""
BLOOMPLAY CONTROLS
SPACE  Pause / Resume
N      Next video
B      Previous video
UP/DOWN Change volume
M      Mute / Unmute
F      Toggle fullscreen
H      Show recent history
L      Select playlist
S      Search videos
R      Refresh library
C      Clear playback history
1      Shuffle mode
2      Sequential mode
3      Repeat current video
Q      Quit
        """)

    def play(self, video, add_session=True, add_history=True):
        if not Path(video["path"]).is_file():
            print("This video is no longer available.")
            logging.warning("Missing video: %s", video["path"])
            return False
        try:
            self.player.play(video)
        except Exception as error:
            logging.exception("Could not play %s", video["path"])
            print(f"Could not play {Path(video['path']).name}: {error}")
            return False

        if add_session:
            if self.session_index < len(self.session) - 1:
                self.session = self.session[:self.session_index + 1]
            self.session.append(video)
            self.session_index = len(self.session) - 1

        if add_history:
            self.history.add(video)

        print(f"\nNow playing: {Path(video['path']).name} [{video['playlist']}]")
        return True

    def next_video(self):
        candidates = self.filtered_library
        if not candidates:
            print("No videos in the current selection.")
            return

        current = self.player.current_video
        if self.mode == "repeat" and current and Path(current["path"]).is_file():
            self.play(current, add_session=False)
            return

        if self.mode == "sequential":
            current_path = Path(current["path"]) if current else None
            ordered = candidates
            start = next((i for i, item in enumerate(ordered) if item["path"] == current_path), -1)
            selected = ordered[(start + 1) % len(ordered)]
        else:
            current_path = Path(current["path"]) if current else None
            choices = [item for item in candidates if item["path"] != current_path]
            selected = random.choice(choices or candidates)

        self.play(selected)

    def previous_video(self):
        if self.session_index <= 0:
            print("No previous video in this session.")
            return
        self.session_index -= 1
        self.play(self.session[self.session_index], add_session=False)

    def show_history(self):
        items = self.history.existing_items()
        print("\nRECENTLY PLAYED")
        if not items:
            print("History is empty.")
            return
        for index, item in enumerate(items[:20], 1):
            print(f"{index:>2}. {Path(item['path']).name}  [{item.get('playlist', 'Unknown')}]  {item.get('played_at', '')}")
        self.prompt_history_selection(items)

    def prompt_history_selection(self, items):
        self.pause_listener()
        try:
            answer = input("Enter a history number to play, or press Enter to return: ").strip()
            if answer.isdigit() and 1 <= int(answer) <= min(20, len(items)):
                item = items[int(answer) - 1]
                video_path = Path(item["path"])
                video = next((v for v in self.library if v["path"] == video_path), None)
                if video is None and video_path.is_file():
                    video = {"path": video_path, "playlist": item.get("playlist", "History")}
                if video:
                    self.play(video)
        finally:
            self.resume_listener()

    def select_playlist(self):
        names = playlists(self.library)
        print("\nPLAYLISTS")
        for index, name in enumerate(names, 1):
            count = sum(1 for video in self.library if video["playlist"] == name)
            print(f"{index}. {name} ({count} videos)")
        print(f"{len(names) + 1}. All videos")
        self.pause_listener()
        try:
            answer = input("Choose a playlist: ").strip()
            if answer.isdigit():
                choice = int(answer)
                if 1 <= choice <= len(names):
                    selected = names[choice - 1]
                    self.filtered_library = [v for v in self.library if v["playlist"] == selected]
                    print(f"Selected playlist: {selected}")
                elif choice == len(names) + 1:
                    self.filtered_library = self.library[:]
                    print("Selected all videos.")
        finally:
            self.resume_listener()

    def search(self):
        self.pause_listener()
        try:
            query = input("Search video name: ").strip()
            results = search_videos(self.library, query)
            if not results:
                print("No matching videos.")
                return
            for index, video in enumerate(results[:30], 1):
                print(f"{index}. {video['path'].name} [{video['playlist']}]")
            answer = input("Enter a number to play, or press Enter to cancel: ").strip()
            if answer.isdigit() and 1 <= int(answer) <= min(30, len(results)):
                selected = results[int(answer) - 1]
                self.filtered_library = results
                self.play(selected)
        finally:
            self.resume_listener()

    def refresh_library(self):
        current_path = self.player.current_video["path"] if self.player.current_video else None
        self.library = scan_videos(self.video_folder)
        self.filtered_library = self.library[:]
        print(f"Library refreshed: {len(self.library)} videos.")
        if current_path and not Path(current_path).is_file():
            print("The currently playing file is no longer in the library.")

    def clear_history(self):
        self.pause_listener()
        try:
            answer = input("Clear all playback history? (y/N): ").strip().lower()
            if answer == "y":
                self.history.clear()
                print("Playback history cleared.")
        finally:
            self.resume_listener()

    def pause_listener(self):
        if self.listener:
            self.listener.stop()
            self.listener.join(timeout=1)
            self.listener = None

    def resume_listener(self):
        if self.running and self.listener is None:
            self.listener = start_listener(self.queue)

    def handle(self, command):
        if command == "PAUSE":
            self.player.toggle_pause()
        elif command == "NEXT" or command == "AUTO_NEXT":
            self.next_video()
        elif command == "BACK":
            self.previous_video()
        elif command == "VOLUME_UP":
            print(f"Volume: {self.player.set_volume(self.player.volume + 5)}%")
        elif command == "VOLUME_DOWN":
            print(f"Volume: {self.player.set_volume(self.player.volume - 5)}%")
        elif command == "MUTE":
            print("Muted." if self.player.toggle_mute() else "Unmuted.")
        elif command == "FULLSCREEN":
            print("Fullscreen enabled." if self.player.toggle_fullscreen() else "Fullscreen disabled.")
        elif command == "HISTORY":
            self.show_history()
        elif command == "PLAYLISTS":
            self.select_playlist()
        elif command == "SEARCH":
            self.search()
        elif command == "REFRESH":
            self.refresh_library()
        elif command == "CLEAR_HISTORY":
            self.clear_history()
        elif command.startswith("MODE_"):
            self.mode = command.removeprefix("MODE_").lower()
            print(f"Playback mode: {self.mode}")
        elif command == "PLAYBACK_ERROR":
            print("Playback error. Skipping to the next video.")
            logging.error("Playback error; skipping current video.")
            self.next_video()
        elif command == "QUIT":
            self.running = False

    def run(self):
        if not self.library:
            print(f"No videos found in: {self.video_folder}")
            print("Edit video_folder in ~/.bloomplay/config.json")
            return

        print(f"Bloomplay 1.0.0 | {len(self.library)} videos found")
        print(f"Video folder: {self.video_folder}")
        self.print_help()
        self.listener = start_listener(self.queue)

        try:
            if self.config["resume_last_video"]:
                recent = self.history.existing_items()
                if recent:
                    path = Path(recent[0]["path"])
                    video = next((v for v in self.library if v["path"] == path), None)
                    if video:
                        self.play(video)
            if self.player.current_video is None:
                self.next_video()

            while self.running:
                try:
                    command = self.queue.get(timeout=0.15)
                    self.handle(command)
                except Empty:
                    pass
        except KeyboardInterrupt:
            print("\nStopping Bloomplay...")
        finally:
            self.running = False
            self.pause_listener()
            self.save_settings()
            self.player.stop()
            print("Bloomplay closed.")

def main():
    try:
        Bloomplay().run()
    except Exception:
        logging.exception("Fatal Bloomplay error")
        raise

if __name__ == "__main__":
    main()

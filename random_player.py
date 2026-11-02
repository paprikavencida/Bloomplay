import os
import random
import vlc
import time
import threading
import queue

# CONFIGURATION
VIDEO_FOLDER = r"C:\Users\YourUser\Videos"

VIDEO_FORMATS = (
    ".mp4",
    ".mkv",
    ".avi",
    ".mov",
    ".wmv",
    ".webm",
    ".flv"
)

# FIND PLAYLISTS
def get_playlists():
    playlists = {}

    for folder in os.listdir(VIDEO_FOLDER):
        folder_path = os.path.join(VIDEO_FOLDER, folder)

        if os.path.isdir(folder_path):
            videos = []

            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    if file.lower().endswith(VIDEO_FORMATS):
                        videos.append(os.path.join(root, file))

            if videos:
                playlists[folder] = videos

    return playlists


# LOAD PLAYLISTS
playlists = get_playlists()

videos = []

for playlist_name, playlist_videos in playlists.items():
    for video in playlist_videos:
        videos.append((video, playlist_name))

if not videos:
    print("No videos found!")
    exit()

print("Bloomplay - Random Video Player")
print("--------------------------------")

for name, playlist in playlists.items():
    print(f"{name}: {len(playlist)} videos")

print("--------------------------------")
print(f"Total videos: {len(videos)}")


# PLAYER SETUP
player_instance = vlc.Instance()
player = player_instance.media_player_new()

command_queue = queue.Queue()

history = []
history_index = -1

paused = False
running = True


# INPUT CONTROLS
def input_controls():
    while running:
        try:
            command = input(
                "\nCommands [P]ause | [N]ext | [B]ack | [Q]uit: "
            ).lower().strip()

            command_queue.put(command)

        except EOFError:
            break


input_thread = threading.Thread(
    target=input_controls,
    daemon=True
)

input_thread.start()


# SELECT RANDOM VIDEO
def get_random_video(current=None):
    available = [
        video for video in videos
        if video != current
    ]

    return random.choice(available)


# PLAY VIDEO
def play_video(video):
    global paused

    file_path, playlist_name = video

    print("\n--------------------------------")
    print(f"Playlist: {playlist_name}")
    print(f"Now playing: {os.path.basename(file_path)}")
    print("--------------------------------")

    media = player_instance.media_new(file_path)
    player.set_media(media)

    paused = False
    player.play()


# START PLAYBACK
current_video = get_random_video()

history.append(current_video)
history_index = 0

play_video(current_video)


# MAIN LOOP
while running:

    # CHECK COMMANDS
    try:
        command = command_queue.get_nowait()

        if command == "p":
            if paused:
                player.play()
                paused = False
                print("Playback resumed.")
            else:
                player.pause()
                paused = True
                print("Playback paused.")

        elif command == "n":
            print("Skipping video...")

            if history_index < len(history) - 1:
                history = history[:history_index + 1]

            current_video = get_random_video(current_video)

            history.append(current_video)
            history_index += 1

            play_video(current_video)

        elif command == "b":
            if history_index > 0:
                history_index -= 1
                current_video = history[history_index]

                print("Returning to previous video...")
                play_video(current_video)
            else:
                print("No previous video.")

        elif command == "q":
            print("Closing Bloomplay...")
            running = False
            break

        else:
            if command:
                print("Unknown command.")

    except queue.Empty:
        pass

    # CHECK PLAYBACK STATE
    state = player.get_state()

    if state == vlc.State.Ended or state == vlc.State.Error:

        if state == vlc.State.Error:
            print("Playback error. Skipping video...")

        if history_index < len(history) - 1:
            history = history[:history_index + 1]

        current_video = get_random_video(current_video)

        history.append(current_video)
        history_index += 1

        play_video(current_video)

    time.sleep(0.2)


# SHUTDOWN
player.stop()
player.release()
player_instance.release()

print("Bloomplay closed.")
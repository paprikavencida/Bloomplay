import os
import random
import vlc
import time

# CONFIG
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

# FIND VIDEOS
def get_videos():
    videos = []

    for file in os.listdir(VIDEO_FOLDER):
        if file.lower().endswith(VIDEO_FORMATS):
            videos.append(os.path.join(VIDEO_FOLDER, file))

    return videos


# PLAYER
videos = get_videos()

if not videos:
    print("No videos found in the folder!")
    exit()

player_instance = vlc.Instance()
player = player_instance.media_player_new()

last_video = None

print(f"{len(videos)} videos found.")
print("Starting random playback...\n")

while True:

    # Select a random video
    available_videos = [
        video for video in videos
        if video != last_video
    ]

    selected_video = random.choice(available_videos)

    last_video = selected_video

    print(f"Now playing: {os.path.basename(selected_video)}")

    # Load video
    media = player_instance.media_new(selected_video)
    player.set_media(media)

    # Start playback
    player.play()

    # Wait until the video finishes
    while True:
        state = player.get_state()

        if state == vlc.State.Ended:
            break

        if state == vlc.State.Error:
            print("Playback error.")
            break

        time.sleep(0.5)

    # Short delay
    time.sleep(1)
from pynput import keyboard

KEYS = {
    "n": "NEXT",
    "b": "BACK",
    "m": "MUTE",
    "f": "FULLSCREEN",
    "h": "HISTORY",
    "l": "PLAYLISTS",
    "s": "SEARCH",
    "r": "REFRESH",
    "c": "CLEAR_HISTORY",
    "q": "QUIT",
    "1": "MODE_SHUFFLE",
    "2": "MODE_SEQUENTIAL",
    "3": "MODE_REPEAT"
}

def start_listener(command_queue):
    def on_press(key):
        if key == keyboard.Key.space:
            command_queue.put("PAUSE")
        elif key == keyboard.Key.up:
            command_queue.put("VOLUME_UP")
        elif key == keyboard.Key.down:
            command_queue.put("VOLUME_DOWN")
        elif getattr(key, "char", None):
            command = KEYS.get(key.char.lower())
            if command:
                command_queue.put(command)

    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    return listener

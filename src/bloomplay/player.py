import logging
import time
import vlc

class VideoPlayer:
    def __init__(self, volume=70, fullscreen=True, event_queue=None):
        self.logger = logging.getLogger("bloomplay")
        self.instance = vlc.Instance()
        if self.instance is None:
            raise RuntimeError("Could not initialize VLC. Check your VLC installation.")
        self.player = self.instance.media_player_new()
        self.volume = volume
        self.fullscreen = fullscreen
        self.muted = False
        self.event_queue = event_queue
        self.current_video = None
        self._ended_event = vlc.EventType.MediaPlayerEndReached
        self._error_event = vlc.EventType.MediaPlayerEncounteredError
        manager = self.player.event_manager()
        manager.event_attach(self._ended_event, self._on_end)
        manager.event_attach(self._error_event, self._on_error)

    def _on_end(self, event):
        if self.event_queue is not None:
            self.event_queue.put("AUTO_NEXT")

    def _on_error(self, event):
        self.logger.error("VLC reported a playback error.")
        if self.event_queue is not None:
            self.event_queue.put("PLAYBACK_ERROR")

    def play(self, video):
        path = str(video["path"])
        media = self.instance.media_new(path)
        self.player.set_media(media)
        result = self.player.play()
        if result == -1:
            raise RuntimeError(f"VLC could not start: {path}")
        self.current_video = video
        time.sleep(0.25)
        self.player.audio_set_volume(self.volume)
        self.player.audio_set_mute(self.muted)
        self.player.set_fullscreen(self.fullscreen)

    def toggle_pause(self):
        state = self.player.get_state()
        if state == vlc.State.Playing:
            self.player.pause()
        elif state == vlc.State.Paused:
            self.player.play()

    def set_volume(self, value):
        self.volume = max(0, min(100, int(value)))
        self.player.audio_set_volume(self.volume)
        if self.muted:
            self.muted = False
            self.player.audio_set_mute(False)
        return self.volume

    def toggle_mute(self):
        self.muted = not self.muted
        self.player.audio_set_mute(self.muted)
        return self.muted

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self.player.set_fullscreen(self.fullscreen)
        return self.fullscreen

    def stop(self):
        try:
            self.player.stop()
        finally:
            self.player.release()
            self.instance.release()

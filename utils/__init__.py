from ffprobe import FFProbe
import subprocess

class VideoMeta:
    def __init__(self, videopath):
        self.videopath = videopath
        self.metadata = FFProbe(videopath)

    def n_frames(self):
        return self.metadata.video[0].frames()

    def n_secs(self):
        return self.metadata.video[0].duration_seconds()

    def pixel_format(self):
        return self.metadata.video[0].pixel_format()

    def bit_rate(self):
        return self.metadata.video[0].bit_rate()

    def fps(self):
        return self.metadata.video[0].framerate
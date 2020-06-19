from matplotlib.pyplot import rcParams
from matplotlib.animation import writers

class FFMPEG_Writer(object):
    def __init__(self, fps = 60, artist = 'Default', bitrate = 4000):
        rcParams['animation.ffmpeg_path'] = 'C:/Users/Public/Documents/WinDS PRO/emu/BizHawk_153/dll/ffmpeg.exe'
        self.writer = writers['ffmpeg']
        self.writer = self.writer(fps = fps, metadata = dict(artist = artist), bitrate = bitrate)

    def getWriter(self):
        return self.writer

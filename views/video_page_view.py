import gi

from utils.find_child import FindChild
from utils.repeated_timer import RepeatedTimer

gi.require_version("Gtk", "3.0")
gi.require_version("Gst", "1.0")
from gi.repository import Gtk, Gst, Gdk

Gst.init(None)


@Gtk.Template(filename="templates/xml/videoDetail.xml")
class VideoPageView(Gtk.Box):
    __gtype_name__ = "detail"
    video = None
    parentWindow = None
    aspect = None
    data = None
    duration = 0
    repeatedTimer = None

    is_playing = False

    def __init__(self, video, window):
        super().__init__()
        self.is_playing = False
        self.video = video
        self.parentWindow = window
        self.connect("realize", self._on_realize)
        self.init_controls()

    def init_controls(self):
        self.aspect = FindChild.find_child(self, "aspect")
        self.repeatedTimer = RepeatedTimer(0.1, self.run_timer)

    def _on_realize(self, widget):
        sink = Gst.ElementFactory.make("gtksink", "sink")
        self.playbin = Gst.ElementFactory.make("playbin", "bin")
        self.playbin.set_property("video-sink", sink)
        self.playbin.set_property("uri", "file://" + self.video.fullPath)
        self.aspect.add(sink.props.widget)
        sink.props.widget.show()
        bus = self.playbin.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        bus.connect("message::eos", self.on_eos)

    def init_video(self):
        self.parentWindow.lblDuration.set_text(self.video.get_formated_duration())
        self.parentWindow.lblCurrentTime.set_text("0:00")
        self.parentWindow.scaleDuration.get_adjustment().set_upper(self.video.duration_in_seconds + 1)
        self.parentWindow.scaleDuration.get_adjustment().set_value(0)
        self.stop()
        self.pause()

    def seek_to_time(self, time_nanoseconds):
        self.playbin.seek(1.0, Gst.Format.TIME, (Gst.SeekFlags.FLUSH | Gst.SeekFlags.ACCURATE),
                          Gst.SeekType.SET, time_nanoseconds,
                          Gst.SeekType.NONE, -1)
        self.duration = time_nanoseconds / 1000000000
        self.parentWindow.lblCurrentTime.set_text(self.get_formated_duration())

    def start(self):
        self.parentWindow.scaleDuration.get_adjustment().set_value(self.duration)
        self.parentWindow.lblCurrentTime.set_text(self.get_formated_duration())
        self.is_playing = True
        self.repeatedTimer.start()
        self.playbin.set_state(Gst.State.PLAYING)

    def pause(self):
        self.is_playing = False
        self.playbin.set_state(Gst.State.PAUSED)
        self.repeatedTimer.stop()

    def stop(self):
        self.is_playing = False
        self.playbin.set_state(Gst.State.NULL)
        self.duration = 0
        self.repeatedTimer.stop()

    def on_eos(self, arg1, arg2):
        self.parentWindow.btnPlay.set_visible(True)
        self.parentWindow.btnPause.set_visible(False)
        self.is_playing = False
        self.stop()
        self.pause()
        self.duration = 0

    def run_timer(self):
        self.duration = self.duration + 0.1
        self.parentWindow.scaleDuration.get_adjustment().set_value(self.duration)
        self.parentWindow.lblCurrentTime.set_text(self.get_formated_duration())

    def get_formated_duration(self):
        hours = int(self.duration) / 3600
        minutes = int(self.duration % 3600) / 60
        seconds = int(self.duration) % 60
        return str(int(minutes)) + ":" + str(seconds if seconds > 9 else "0" + str(seconds))

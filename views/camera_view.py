import gi

from utils.find_child import FindChild

gi.require_version("Gtk", "3.0")
gi.require_version("Gst", "1.0")
from gi.repository import Gtk, Gst, GLib

# Needed for window.get_xid(), xvimagesink.set_window_handle(), respectively:
gi.require_version("GstVideo", "1.0")
gi.require_version("GdkX11", "3.0")
from gi.repository import GdkX11, GstVideo

Gst.init(None)


@Gtk.Template(filename="templates/xml/cameraView.xml")
class CameraDetail(Gtk.Box):
    __gtype_name__ = "cameraView"

    parentWindow = None

    def __init__(self, window):
        super().__init__()
        self.parentWindow = window
        self.init_controls()
        self.connect("realize", self._on_realize)
        self.init_state()

    def init_state(self):
        self.parentWindow.btnRec.set_visible(True)

    def init_controls(self):
        self.btnRec = FindChild.find_child(self, "btnRec")

    def _on_realize(self, widget):
        self.init_main_pipeline()

    def init_main_pipeline(self):
        self.mainpipeline = Gst.Pipeline()
        main_source = Gst.ElementFactory.make("v4l2src")
        self.main_tee = Gst.ElementFactory.make("tee")
        self.main_tee.set_property("name", "t")

        self.mainpipeline.add(main_source)
        self.mainpipeline.add(self.main_tee)

        main_source.link(self.main_tee)

        self.init_record_pipeline()
        # self.init_play_pipeline()

    def init_play_pipeline(self):
        self.queue_play = Gst.ElementFactory.make("queue")
        jpegdec_play = Gst.ElementFactory.make("jpegdec")
        videoconvert_play = Gst.ElementFactory.make("videoconvert")
        self.sink_play = Gst.ElementFactory.make("gtksink")
        self.sink_play.set_property("sync", False)

        self.mainpipeline.add(self.queue_play)
        self.mainpipeline.add(jpegdec_play)
        self.mainpipeline.add(videoconvert_play)
        self.mainpipeline.add(self.sink_play)

        self.main_tee.link(self.queue_record)
        self.queue_play.link(jpegdec_play)
        jpegdec_play.link(videoconvert_play)
        videoconvert_play.link(self.sink_play)

        self.pack_start(self.sink_play.props.widget, True, True, 0)
        self.sink_play.props.widget.show()

    def init_record_pipeline(self):
        self.queue_record = Gst.ElementFactory.make("queue")
        jpegdec_record = Gst.ElementFactory.make("jpegdec")
        videoconvert_record = Gst.ElementFactory.make("videoconvert")
        x264enc_record = Gst.ElementFactory.make("x264enc")
        x264enc_record.set_property("tune", "zerolatency")
        mp4mux_record = Gst.ElementFactory.make("mp4mux")
        sink_record = Gst.ElementFactory.make("filesink")
        sink_record.set_property("location", "output.mp4")
        audiotestsrc_record = Gst.ElementFactory.make("audiotestsrc")
        lamemp3enc_record = Gst.ElementFactory.make("lamemp3enc")

        self.mainpipeline.add(self.queue_record)
        self.mainpipeline.add(jpegdec_record)
        self.mainpipeline.add(x264enc_record)
        self.mainpipeline.add(mp4mux_record)
        self.mainpipeline.add(videoconvert_record)
        self.mainpipeline.add(sink_record)
        self.mainpipeline.add(audiotestsrc_record)
        self.mainpipeline.add(lamemp3enc_record)

        self.main_tee.link(self.queue_record)
        self.queue_record.link(jpegdec_record)
        jpegdec_record.link(videoconvert_record)
        videoconvert_record.link(x264enc_record)
        x264enc_record.link(mp4mux_record)
        mp4mux_record.link(sink_record)
        sink_record.link(lamemp3enc_record)
        sink_record.link(audiotestsrc_record)
        lamemp3enc_record.link(mp4mux_record)

    def start_image(self):
        self.mainpipeline.set_state(Gst.State.PLAYING)

    def stop_image(self):
        self.mainpipeline.set_state(Gst.State.NULL)

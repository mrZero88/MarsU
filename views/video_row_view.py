import gi

from utils.find_child import FindChild

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


@Gtk.Template(filename="templates/xml/videoRow.xml")
class VideoRowView(Gtk.Box):
    __gtype_name__ = "row"
    video = None
    page_name = ""

    def __init__(self, video):
        super().__init__()
        self.video = video
        self.bind_data()

    def bind_data(self):
        lbl_date = FindChild.find_child(self, "lblDate")
        lbl_duration = FindChild.find_child(self, "lblDuration")
        img_thumbnail = FindChild.find_child(self, "imgThumbnail")
        lbl_date.set_label(self.video.get_formated_date())
        lbl_duration.set_label(self.video.get_formated_time())
        img_thumbnail.set_from_file("img/video_thumbnails/" + self.video.thumbnailName)

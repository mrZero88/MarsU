import asyncio
import warnings

import gi

warnings.filterwarnings("ignore", category=DeprecationWarning)

gi.require_version("Notify", "0.7")
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import GdkPixbuf, Notify


class Notification:

    @staticmethod
    def show_notification(title, body, icon_file_path):
        image = GdkPixbuf.Pixbuf.new_from_file(icon_file_path)
        Notify.init(title)
        n = Notify.Notification.new(title, body)
        n.set_icon_from_pixbuf(image)
        n.set_image_from_pixbuf(image)
        n.show()

#!/usr/bin/env python3

import gi

from views.camera_view import CameraDetail
from viewmodels.main_view_model import MainViewModel
from utils.find_child import FindChild

gi.require_version("Gtk", "3.0")
gi.require_version('Notify', '0.7')
from gi.repository import Gtk, Notify

gi.require_version("Gdk", "3.0")
from gi.repository import Gdk


@Gtk.Template(filename="templates/xml/mainView.xml")
class MainView(Gtk.Window):
    __gtype_name__ = "window"

    # Main View Model
    mainViewModel = None
    selected_video_index = -1

    # Containers
    videoList = None
    stackDetail = None

    # Ui Elements
    cameraView = None
    scaleAdjustment = None
    btnRec = None
    btnPlay = None
    btnPause = None
    lblCurrentTime = None
    lblDuration = None
    scaleDuration = None
    aspect = None

    @Gtk.Template.Callback()
    def on_show(self, _):
        self.init()

        self.mainViewModel = MainViewModel(self)

        self.add_pages_to_ui(self.mainViewModel.get_pages())

        self.add_videos_to_ui(self.mainViewModel.get_videos())

    def init(self):
        self.init_controls()
        self.hide_all_controls()
        # Notification.show_notification("Mars", "Welcome back, " + self.user.first_name + "!",
        #                              "img/app_icon/mars64.png")

    def init_controls(self):
        self.stackDetail = FindChild.find_child(self, "stackDetail")
        self.videoList = FindChild.find_child(self, "videoList")
        self.btnRec = FindChild.find_child(self, "btnRec")
        self.btnPlay = FindChild.find_child(self, "btnPlay")
        self.btnPause = FindChild.find_child(self, "btnPause")
        self.scaleDuration = FindChild.find_child(self, "scaleDuration")
        self.lblCurrentTime = FindChild.find_child(self, "lblCurrentTime")
        self.lblDuration = FindChild.find_child(self, "lblDuration")
        self.cameraView = CameraDetail(self)

    def add_pages_to_ui(self, pages):
        self.stackDetail.add(self.cameraView)

    def add_videos_to_ui(self, videos):
        video_rows = self.mainViewModel.get_video_rows()
        video_pages = self.mainViewModel.get_video_pages()
        for i in range(0, len(videos)):
            self.stackDetail.add(video_pages[i])
            self.videoList.add(video_rows[i])

    @Gtk.Template.Callback()
    def on_row_selected(self, *args):
        if args[1] is None:
            return

        self.cameraView.stop_image()
        self.show_video_controls()
        selected_index = args[1].get_index()
        self.mainViewModel.set_selected_index(selected_index)
        previous_video_page = self.mainViewModel.get_video_pages()[self.selected_video_index]
        previous_video_page.stop()
        video_page = self.mainViewModel.get_selected_video_page()
        self.stackDetail.set_visible_child(video_page)
        video_page.init_video()
        self.selected_video_index = selected_index

    @Gtk.Template.Callback()
    def on_scale_value_changed(self, element):
        video_page = self.mainViewModel.get_selected_video_page()
        if not video_page.is_playing:
            value = int(element.get_value() * 1000000000)
            video_page.seek_to_time(value)

    """
        On Pages Clicked
    """

    @Gtk.Template.Callback()
    def on_settings_clicked(self, *args):
        self.hide_all_controls()
        self.show_settings_controls()
        self.mainViewModel.get_selected_video_page().stop()
        self.remove_stack_detail_selection()
        self.stackDetail.set_visible_child_name("settingsPage")

    @Gtk.Template.Callback()
    def on_camera_clicked(self, *args):
        self.hide_all_controls()
        self.show_camera_controls()
        # self.mainViewModel.get_selected_video_page().stop()
        self.remove_stack_detail_selection()
        self.stackDetail.set_visible_child(self.cameraView)
        self.cameraView.start_image()

    @Gtk.Template.Callback()
    def on_play_clicked(self, *args):
        self.btnPlay.set_visible(False)
        self.btnPause.set_visible(True)
        self.mainViewModel.get_selected_video_page().start()

    @Gtk.Template.Callback()
    def on_pause_clicked(self, *args):
        self.btnPlay.set_visible(True)
        self.btnPause.set_visible(False)
        self.mainViewModel.get_selected_video_page().stop()

    def remove_stack_detail_selection(self):
        self.videoList.unselect_all()
        self.selected_video_index = -1

    @Gtk.Template.Callback()
    def on_key_pressed(self, widget, event):
        key_val = event.get_keyval()[1]
        # Space Key
        if key_val == 32:
            video_page = self.mainViewModel.get_selected_video_page()
            if not video_page.is_playing:
                self.on_play_clicked()
            else:
                self.on_pause_clicked()
        # Delete Key
        elif key_val == 65535:
            self.open_delete_video_dialog()

    """
        Delete Video
    """

    def open_delete_video_dialog(self):
        dialog = Gtk.MessageDialog(transient_for=self, flags=Gtk.DialogFlags.MODAL,
                                   message_type=Gtk.MessageType.WARNING,
                                   buttons=Gtk.ButtonsType.YES_NO, text="Are you sure you want to delete this video?")
        response = dialog.run()
        if response == Gtk.ResponseType.YES:
            self.delete_video()
        dialog.destroy()

    def delete_video(self):
        video = self.mainViewModel.get_selected_video()
        video_page = self.mainViewModel.get_selected_video_page()
        video_listbox_row = self.videoList.get_children()[self.selected_video_index]
        self.selected_video_index = -1
        self.stackDetail.remove(video_page)
        self.videoList.remove(video_listbox_row)
        self.mainViewModel.videos.remove(video)
        self.mainViewModel.video_pages.remove(video_page)

    """
        Show/Hide Methods
    """

    def hide_all_controls(self):
        self.hide_video_controls()
        self.hide_camera_controls()
        self.hide_settings_controls()

    def hide_video_controls(self):
        self.btnPlay.set_visible(False)
        self.btnPause.set_visible(False)
        self.scaleDuration.set_visible(False)
        self.lblDuration.set_visible(False)
        self.lblCurrentTime.set_visible(False)

    def hide_camera_controls(self):
        self.btnRec.set_visible(False)

    def hide_settings_controls(self):
        print("Settings Controls Hidden")

    def show_video_controls(self):
        self.hide_all_controls()
        self.btnPlay.set_visible(True)
        self.btnPause.set_visible(False)
        self.scaleDuration.set_visible(True)
        self.lblDuration.set_visible(True)
        self.lblCurrentTime.set_visible(True)

    def show_camera_controls(self):
        self.btnRec.set_visible(True)

    def show_settings_controls(self):
        print("Settings Controls Shown")

    @Gtk.Template.Callback()
    def on_destroy(self, *args):
        if self.selected_video_index != -1:
            self.mainViewModel.get_selected_video_page().stop()
        Notify.uninit()
        Gtk.main_quit()


window = MainView()
screen = Gdk.Screen.get_default()
provider = Gtk.CssProvider()
provider.load_from_path("styles/scrolledWindow.css")
Gtk.StyleContext.add_provider_for_screen(screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
window.show()
Gtk.main()

import sys

from views.video_page_view import VideoPageView
from views.video_row_view import VideoRowView
from core.page_manager import PageManager
from core.user_manager import UserManager
from core.video_manager import VideoManager
from tinydb import TinyDB


class MainViewModel:
    PROJECT_ROOT = sys.path[1]

    # Parent Window
    window = None
    # List of pages of the app
    pages = []
    # List of videos of the app
    videos = []
    # Selected Video
    selected_video = None
    # List of video pages
    video_pages = []
    # Selected Page
    selected_page = None
    # List of video rows
    video_rows = []
    # Selected video row
    selected_video_row = None
    # User
    user = None
    # Database
    db = None

    def __init__(self, window):
        self.window = window
        self.db = TinyDB(MainViewModel.PROJECT_ROOT + "/database/db.json")
        self.load_user()
        self.load_pages()
        self.load_videos()
        self.create_video_pages_and_rows()

    def load_user(self):
        um = UserManager(self.db)
        um.load_user()
        self.user = um.get_user()

    def load_pages(self):
        pm = PageManager()
        pm.load_pages()
        self.pages = pm.get_pages()

    def create_video_pages_and_rows(self):
        for video in self.videos:
            video_row = VideoRowView(video)
            video_page = VideoPageView(video, self.window)
            self.video_rows.append(video_row)
            self.video_pages.append(video_page)

    def load_videos(self):
        vm = VideoManager("/home/danielcorreia/OneDrive/Flyzerosky/videos", self.db)
        vm.load_videos()
        self.videos = vm.get_videos()

    def set_selected_index(self, index):
        self.selected_video = self.videos[index]
        self.selected_page = self.video_pages[index]
        self.selected_video_row = self.video_rows[index]

    def get_videos(self):
        return self.videos

    def get_pages(self):
        return self.pages

    def get_video_rows(self):
        return self.video_rows

    def get_video_pages(self):
        return self.video_pages

    def get_selected_video_page(self):
        return self.selected_page

    def get_selected_video(self):
        return self.selected_video

    def get_selected_video_row(self):
        return self.selected_video_row

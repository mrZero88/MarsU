import json
from os import listdir
from os.path import isfile, join

from models.video import Video
from utils.file_video_converter import FileVideoConverter


class VideoManager:

    def __init__(self, path, db):
        self.db = db
        self.videosTable = self.db.table(path)
        self.path = path
        self.videos = []

    def load_videos(self):
        if self.exists_videos():
            self.load_videos_from_database()
        else:
            self.load_videos_from_directory()
            self.insert_videos_in_database()

    def insert_videos_in_database(self):
        for video in self.videos:
            self.videosTable.insert(video)

    def exists_videos(self):
        return True if self.videosTable.all() else False

    def load_videos_from_database(self):
        json_string = json.dumps(self.videosTable.all())
        self.videos = json.loads(json_string, object_hook=Video.object_decoder)

    def load_videos_from_directory(self):
        video_file_names = sorted([f for f in listdir(self.path) if isfile(join(self.path, f))], reverse=True)
        for video_file_name in video_file_names:
            self.videos.append(
                FileVideoConverter.convert_file_to_video(video_file_name, self.path + "/" + video_file_name,
                                                         video_file_name, "png"))

    def get_videos(self):
        return self.videos

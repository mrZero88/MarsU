import datetime

from utils.command import Command
from datetime import datetime


class Video(dict):
    def __init__(self, file_name, full_path, created_date_time, duration_in_seconds, thumbnail_name):
        dict.__init__(self, file_name=file_name, full_path=full_path,
                      created_date_time=created_date_time,
                      duration_in_seconds=duration_in_seconds, thumbnail_name=thumbnail_name)
        self.fileName = file_name
        self.fullPath = full_path
        self.created_date_time = created_date_time
        self.duration_in_seconds = duration_in_seconds
        self.thumbnailName = thumbnail_name

    def set_duration_in_seconds(self):
        command = "ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 " + \
                  self.fullPath
        output = Command.run_command_with_output_pipe(command)
        self.duration_in_seconds = int(float(output.stdout))

    def get_formated_date(self):
        dt = datetime.utcfromtimestamp(self.created_date_time)
        return dt.strftime("%d %b %y")

    def get_formated_time(self):
        dt = datetime.utcfromtimestamp(self.created_date_time)
        return dt.strftime("%H:%M:%S")

    def get_formated_duration(self):
        result = ""
        hours = self.duration_in_seconds / 3600
        minutes = (self.duration_in_seconds % 3600) / 60
        seconds = self.duration_in_seconds % 60
        return str(int(minutes)) + ":" + str(seconds if seconds > 9 else "0" + str(seconds))

    def __repr__(self):
        return "[" + self.fileName + ", " + self.fullPath + ", " + str(self.created_date_time) + ", " + str(
            self.duration_in_seconds) + ", " + self.thumbnailName + "]"

    @staticmethod
    def object_decoder(object_video):
        return Video(object_video["file_name"], object_video["full_path"],
                     object_video["created_date_time"],
                     object_video["duration_in_seconds"],
                     object_video["thumbnail_name"])

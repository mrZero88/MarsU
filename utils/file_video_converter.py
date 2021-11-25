"""
    Class converts file names typed like '21_07_26_08_23_47.mov' into a video object
"""
import datetime
import os
import sys
from datetime import datetime
from os.path import isfile
from models.video import Video
from utils.command import Command


class FileVideoConverter:
    PROJECT_ROOT = sys.path[1]
    THUMBNAILS_PICTURES_PATH = "/img/video_thumbnails/"

    @staticmethod
    def convert_file_to_video(file_name, full_path, thumbnail_file_name, thumbnail_image_type):
        created_date_time = os.path.getmtime(full_path)
        duration_in_seconds = FileVideoConverter.get_duration_in_seconds(full_path)
        thumbnail_file_name = thumbnail_file_name.split(".")[0]
        thumbnail_file_name = thumbnail_file_name + "." + thumbnail_image_type

        if not isfile(
                FileVideoConverter.PROJECT_ROOT + FileVideoConverter.THUMBNAILS_PICTURES_PATH + thumbnail_file_name):
            FileVideoConverter.generate_thumbnail(full_path, thumbnail_file_name)

        return Video(file_name, full_path, created_date_time, duration_in_seconds, thumbnail_file_name)

    @staticmethod
    def get_duration_in_seconds(filename):
        command = "ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 " + filename
        output = Command.run_command_with_output_pipe(command)
        return int(float(output.stdout))

    @staticmethod
    def generate_thumbnail(video_full_path, thumbnail_file_name):
        FileVideoConverter.generate(video_full_path, thumbnail_file_name)

    @staticmethod
    def generate(video_full_path, thumbnail_file_name):
        bash_command = "ffmpeg -i " + video_full_path + \
                       " -r 0.0033 -vf scale=-1:80 -vcodec png " + FileVideoConverter.PROJECT_ROOT + \
                       FileVideoConverter.THUMBNAILS_PICTURES_PATH + \
                       thumbnail_file_name
        Command.run_command(bash_command)

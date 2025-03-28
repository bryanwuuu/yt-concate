from yt_concate.settings import CAPTIONS_DIR, VIDEOS_DIR, DOWNLOADS_DIR
import os

class Utils:
    def __init__(self):
        pass

    @staticmethod
    def get_caption_filepath(video_id):
        return os.path.join(CAPTIONS_DIR, video_id + ".txt")

    def create_dirs(self):
        os.makedirs(DOWNLOADS_DIR,exist_ok=True )
        os.makedirs(VIDEOS_DIR,exist_ok=True )
        os.makedirs(CAPTIONS_DIR,exist_ok=True )

    def caption_file_exists(self,video_id):
        path = self.get_caption_filepath(video_id)
        return os.path.exists(path) and os.path.getsize(path) > 0

    def get_video_list_filepath(self, channel_id):
        return os.path.join(DOWNLOADS_DIR,channel_id + '.txt')

    def video_list_file_exist(self, channel_id):
        path = self.get_video_list_filepath(channel_id)
        return os.path.exists(path) and os.path.getsize(path) > 0
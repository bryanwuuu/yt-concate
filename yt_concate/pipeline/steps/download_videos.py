from .search import Step
import yt_dlp
from pytube import YouTube
from yt_concate.settings import VIDEOS_DIR

class DownloadVideos(Step):
    def process(self, data, inputs, utils):
        print(len(data))
        yt_set = set([found.yt for found in data])
        print(len(yt_set))
        ydl_opts = {
            'writesubtitles': True,  # 下載字幕
            'subtitleslangs': ['en'],  # 指定語言（英文）
            'outtmpl': VIDEOS_DIR + '/%(id)s.%(ext)s',
            'format': 'best',  # ✅ 改這行，避免合併視訊音訊
            'nooverwrites': True,
            'quiet': False,
        }

        for yt in yt_set:
            url = yt.url

            # YouTube(url).streams.first().download(output_path=VIDEOS_DIR , filename=yt.id)

            if utils.video_file_exists(yt):
                print('found existing video file, skipping')
                continue
            print(f"🔍 正在處理影片：{url}")
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
            except Exception as e:
                print(e)
                continue
        return data
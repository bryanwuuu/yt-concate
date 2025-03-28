
import datetime
import json
from urllib.parse import parse_qs, urlparse

from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from yt_concate.pipeline.steps.step import Step
from yt_concate.pipeline.steps.step import StepException
from yt_concate.settings import CAPTIONS_DIR, VIDEOS_DIR
class DownloadCaptions(Step):
    def process(self, data, inputs, utils):
        for yt in data:
            print('Test caption for ', yt.id)
            # source = YouTube(url)
            # en_caption = source.captions.get_by_language_code('en')
            # en_caption_convert_to_srt = (en_caption.generate_srt_captions())
            # query = urlparse(yt.url).query
            # video_id = parse_qs(query)["v"][0]
            if utils.caption_file_exists(yt):
                # print('found existing caption file:' + video_id)
                continue
            print(yt.url)  # 👉 TW-joGuPDQY
            try:
                srt = YouTubeTranscriptApi.get_transcript(yt.id)
            except Exception as e:
                # print(f'exception when downloading caption file {video_id}: {e}')
                continue
            # outputs = json.dumps(srt)
            output = self.convert_to_srt(srt)
            # print(srt)
            # save the caption to a file named Output.txt
            text_file = open(utils.get_caption_filepath(yt.url), "w",encoding='utf-8')
            text_file.write(output)
            text_file.close()
            # break
        return data

    def format_time(self, seconds):
        td = datetime.timedelta(seconds=seconds)
        # 把 timedelta 轉換為 SRT 格式：hh:mm:ss,mmm
        total_seconds = int(td.total_seconds())
        millisec = int((td.total_seconds() - total_seconds) * 1000)
        return str(td)[:-3].replace('.', ',').zfill(12)

    def convert_to_srt(self, subtitles):
        srt_lines = []
        for idx, item in enumerate(subtitles, 1):
            start = self.format_time(item['start'])
            end = self.format_time(item['start'] + item['duration'])
            text = item['text']

            srt_block = f"{idx}\n{start} --> {end}\n{text}\n"
            srt_lines.append(srt_block)

        return '\n'.join(srt_lines)
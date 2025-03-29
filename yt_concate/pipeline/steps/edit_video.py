import os
from yt_concate.pipeline.steps.step import Step
from moviepy import VideoFileClip, TextClip, CompositeVideoClip, concatenate_videoclips
class EditVideo(Step):
    def process(self, data, inputs, utils):
        clips = []
        for found in data:
            print(f"🔍 剪輯時間段: {found.time}")
            try:
                start, end = self.parse_caption_time(found.time)
                video_path = found.yt.video_filepath

                if not os.path.exists(video_path):
                    print(f"🚫 找不到影片檔案：{video_path}")
                    continue

                video_clip = VideoFileClip(video_path)
                video_duration = video_clip.duration
                safe_end = min(end, video_duration)

                if start >= safe_end:
                    print(f"⚠️ 無效時間範圍：start={start}, end={safe_end}")
                    continue

                clip = video_clip.subclipped(start, safe_end)
                # video = VideoFileClip(found.yt.video_filepath).subclipped(start, end)
                clips.append(clip)

                print(f"✅ 成功剪輯：{video_path} [{start:.2f} ~ {safe_end:.2f} 秒]")

                if len(clips) >= inputs['limit']:
                    break

            except Exception as e:
                print(f"❌ 剪輯失敗：{found.yt.video_filepath}，錯誤：{e}")
                continue

        if not clips:
            print("🚨 沒有任何片段可合併，結束。")
            return

        final_clip = concatenate_videoclips(clips)
        filename = utils.get_output_file(inputs['channel_id'], inputs['search_word'])

        print(f"💾 輸出影片：{filename}")
        # final_clip.write_videofile(filename, codec="libx264", audio_codec="aac")

        final_clip.write_videofile(filename)

    def parse_caption_time(self, caption_time):
        start, end = caption_time.split(' --> ')
        return self.parse_time_str(start), self.parse_time_str(end)

    def parse_time_str(self, time_str):
        h, m, s_ms = time_str.strip().split(':')
        s, ms = s_ms.split(',')
        return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000


'''
class EditVideo(Step):
    def process(self, data, inputs, utils):
        clips = []
        for found in data:
            print(found.time)
            start,end = self.parse_caption_time(found.time)
            video =VideoFileClip(found.yt.video_filepath).subclipped(start, end)
            clips.append(video)
            if len(clips) > inputs['limit']:
                break
        final_clip = concatenate_videoclips(clips)
        filename = utils.get_output_file(inputs['channel_id'], inputs['search_word'])
        final_clip.write_videofile(filename)



    def parse_caption_time(self,caption_time):
        start, end = caption_time.split(' --> ')
        return self.parse_time_str(start), self.parse_time_str(end)

    def parse_time_str(self, time_str):
        h,m,s = time_str.split(':')
        s,ms = s.split(',')
        return int(h), int(m), int(s)+int(ms)/1000

if __name__ == '__main__':
    e = EditVideo()

'''
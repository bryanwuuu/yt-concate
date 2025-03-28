from dotenv import load_dotenv
import os
load_dotenv()  # take environment variables

API_KEY = os.getenv("API_KEY")
DOWNLOADS_DIR = 'downloads'
CAPTIONS_DIR = os.path.join(DOWNLOADS_DIR , 'captions')
VIDEOS_DIR = os.path.join(DOWNLOADS_DIR , 'videos')
# VIDEO_LIST_FILENAME ='video_list.txt'

# encoding: utf-8
from moviepy.editor import *

from common.logger import logger
from settings import PWD


class Singer(object):

    def __init__(self):
        pass

    def sing(self, path):
        clip = AudioFileClip(path)
        clip.preview()
        clip.close()

def sing_all():
    with open(PWD + '/song_list.txt', 'r') as f:
        songlist = f.read()
        for item in songlist.split('\n'):
            s = item.split(' ')
            if len(s) == 0:
                continue
            song_name = s[0] if len(s) == 1 else s[1]
            logger.info('sing {} ...'.format(song_name))
            Singer().sing('output/{}.m4a'.format(song_name))
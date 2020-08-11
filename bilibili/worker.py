# encoding: utf-8
import requests
import json

from settings import B_URL, HEADER, PWD
from common.logger import logger

requests.packages.urllib3.disable_warnings()
session = requests.session()



class BWorker(object):
    # TODO support param p
    def __init__(self, bv, name=None):
        self.bv = bv
        self.header = HEADER
        self.name = name


    @property
    def output_path(self):
        return PWD + '/output/{}.m4a'.format(self.name or self.bv)
        # return '../output/{}.mp4'.format(self.bv)

    @property
    def bv_url(self):
        return B_URL + self.bv

    def get_audio_url(self):
        resp = session.get(url=self.bv_url, headers=self.header, verify=False)
        info = json.loads(resp.content.split('<script>')[1][20:-9])
        audio_url = info['data']['dash']['audio'][0]['baseUrl']
        return audio_url

    def download_audio(self):
        download_url = self.get_audio_url()
        # logger.info(download_url)
        # logger.info(self.bv_url)
        self.header.update({'Referer': self.bv_url})
        single_length = 1024 * 512
        begin, end, flag = 0, single_length - 1, 0

        with open(self.output_path, 'wb') as fp:
            while flag == 0:
                self.header.update({'Range': 'bytes=' + str(begin) + '-' + str(end)})
                res = session.get(url=download_url, headers=self.header, verify=False)
                if res.status_code != 416:
                    begin = end + 1
                    end = end + single_length
                else:
                    self.header.update({'Range': str(end + 1) + '-'})
                    res = session.get(url=download_url, headers=self.header, verify=False)
                    flag = 1
                fp.write(res.content)
        fp.close()


def download_songlist():
    with open(PWD + '/song_list.txt', 'r') as f:
        songlist = f.read()
    for item in songlist.split('\n'):
        s = item.split(' ')
        if len(s) == 0:
            continue
        logger.info('download bv {} name {} ...'.format(s[0], 'NULL' if len(s) == 1 else s[1]))
        BWorker(*s).download_audio()
        logger.info('download bv {} name {} completely'.format(s[0], s[1]))

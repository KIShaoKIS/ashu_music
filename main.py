# encoding: utf-8
# import pygame
# import sys
#
#
# pygame.init()
# pygame.mixer.init()
# pygame.mixer.music.load('output/BV1fs411f7Sz.m4a')
# pygame.mixer.music.play(loops=0,start=0)
#
# pygame.display.set_mode([300,300])
#
# pygame.display.update()
#
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             sys.exit()
from bilibili.singer import Singer, sing_all
from bilibili.worker import download_songlist

# download_songlist()
sing_all()
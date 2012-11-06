# -*- coding: utf-8 -*-

import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time

class Browser:
    OKAY = 'OKAY'
    NSFW = 'NSFW'
    REMOVED = 'REMOVED'
    ERROR = 'ERROR'

    def __init__(self):
        #self._browser = webdriver.Firefox()
        pass

    def open_gag(self, gid):
        pass

    def get_status(self):
        return Browser.OKAY

    def get_uploader(self):
        return 'cr4icis'

    def get_title(self):
        return 'Found this above the urinal in the library.'

    def get_image_url(self):
        return 'http://d24w6bsrhbeh9d.cloudfront.net/photo/5761739_700b.jpg'

    def get_basic_num(self):
        num_comments = 39
        num_loved = 9618
        return num_comments, num_loved

    def get_external_num(self):
        num_fb_share = 2340
        num_fb_like = 2500
        num_tweet = 4
        return num_fb_share, num_fb_like, num_tweet

    def get_comments(self):
        return [[('Claudio Arenas-Liotard', True, 'nice try, drug dealer.', 153),
                 ('Johannes Antunes', True, 'i think its just viagra', 10),
                 ('Ashley Moore', True, 'More like rapist', 5)],
                [('David Robles', True, 'Seems like either pill he\'s still gonna show you..."how deep the rabbit hole goes"', 92),
                 ('Joaquin Ampuero Cacic', False, 'like his anus got it?', 1)]
               ]

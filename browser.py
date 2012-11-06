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
    VIDEO = 'VIDEO'

    def __init__(self):
        self._browser = webdriver.Firefox()

    def open_gag(self, gid):
        self._browser.get("http://9gag.com/gag/%07d" % gid)

    def get_status(self):
        try:
            self._browser.find_element_by_id('page-404')
            return Browser.ERROR
        except:
            pass

        try:
            self._browser.find_element_by_class_name('form-message')
            return Browser.REMOVED
        except:
            pass

        try:
            self._browser.find_element_by_class_name('post-info-pad')
        except:
            return Browser.NSFW

        try:
            self._browser.find_element_by_class_name('video-post')
            return Browser.VIDEO
        except:
            pass

        return Browser.OKAY

    def get_info_pad(self):
        info_pad = self._browser.find_element_by_class_name('post-info-pad')
        title = 'Why doesn\'t she understand this?'
        uploader = 'livandale'
        num_comments = 49
        num_loved = 16856
        return title, uploader, num_comments, num_loved

    def get_image_url(self):
        return 'http://d24w6bsrhbeh9d.cloudfront.net/photo/5761739_700b.jpg'

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

    def _wait_some_time(self):
        time.sleep(0.5)


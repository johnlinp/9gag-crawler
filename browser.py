# -*- coding: utf-8 -*-

import re
import mechanize
import cookielib
from BeautifulSoup import BeautifulSoup

class Browser:
    OKAY = 'OKAY'
    NSFW = 'NSFW'
    REMOVED = 'REMOVED'
    ERROR = 'ERROR'
    VIDEO = 'VIDEO'

    def __init__(self):
        self._br = mechanize.Browser()
        self._set_cookie_jar()
        self._set_options()

    def _set_cookie_jar(self):
        cj = cookielib.LWPCookieJar()
        self._br.set_cookiejar(cj)

    def _set_options(self):
        self._br.set_handle_equiv(True)
        self._br.set_handle_redirect(True)
        self._br.set_handle_referer(True)
        self._br.set_handle_robots(False)
        self._br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
        self._br.addheaders = [('User-agent', 
                                '''Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) 
                                Gecko/2008071615 
                                Fedora/3.0.1-1.fc9 
                                Firefox/3.0.1''')]

    def open_gag(self, gid):
        try:
            self._page = self._br.open('http://9gag.com/gag/%07d' % gid)
        except KeyboardInterrupt:
            raise 
        except:
            return Browser.ERROR

        content = self._page.read()
        content = re.sub('/ >', '/>', content)
        self._soup = BeautifulSoup(content)

        if self._soup.find('p', {'class': 'form-message error '}) is not None:
            return Browser.REMOVED

        if self._soup.find('div', {'class': 'post-info-pad'}) is None:
            return Browser.NSFW

        if self._soup.find('div', {'class': 'video-post'}) is not None:
            return Browser.VIDEO

        return Browser.OKAY

    def get_info_pad(self):
        info_pad = self._soup.find('div', {'class': 'post-info-pad'})
        title = info_pad.find('h1').string.encode('utf-8')
        uploader = info_pad.find('p').find('a').string.encode('utf-8')
        num_comments = info_pad.find('span', {'class': 'comment'}).string.encode('utf-8')
        num_loved = info_pad.find('span', {'class': 'loved'}).find('span').string.encode('utf-8')
        return title, uploader.rstrip(), int(num_comments), int(num_loved)

    def get_image_url(self):
        image_url = 'http:' + self._soup.find('div', {'class': 'img-wrap'}).find('img')['src'].encode('utf-8')
        return image_url

    def get_share_num(self):
        num_fb_share = self._soup.find('a', {'class': 'facebook-share-button'}).string.encode('utf-8')
        num_tweet = self._soup.find('a', {'class': 'twitter-tweet-button'}).string.encode('utf-8')
        return int(num_fb_share), int(num_tweet)

    def get_fb_like_num(self):
        return 5566

    def get_comments(self):
        # https://graph.facebook.com/comments/?ids=http://9gag.com/gag/5792194
        return []



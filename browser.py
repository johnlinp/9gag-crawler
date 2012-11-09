# -*- coding: utf-8 -*-

import re, json
import mechanize
import cookielib
from BeautifulSoup import BeautifulSoup

class Browser:
    OKAY = 'OKAY'
    NSFW = 'NSFW'
    REMOVED = 'REMOVED'
    NOT_FOUND = 'NOT_FOUND'
    HTML_MALFORMED = 'HTML_MALFORMED'
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
        self._url = 'http://9gag.com/gag/%d' % gid
        try:
            page = self._br.open(self._url)
        except KeyboardInterrupt:
            raise 
        except:
            return Browser.NOT_FOUND

        content = page.read()
        content = re.sub('/ >', '/>', content) # workaround for strange BeautifulSoup...
        try:
            self._soup = BeautifulSoup(content)
        except:
            return Browser.HTML_MALFORMED

        if self._soup.find('p', {'class': 'form-message error '}) is not None:
            return Browser.REMOVED

        if self._soup.find('div', {'class': 'post-info-pad'}) is None:
            return Browser.NSFW

        if self._soup.find('div', {'class': 'video-post'}) is not None:
            return Browser.VIDEO

        return Browser.OKAY

    def get_info_pad(self):
        info_pad = self._soup.find('div', {'class': 'post-info-pad'})
        title = info_pad.find('h1').string
        title = unicode(title)
        uploader = info_pad.find('p').find('a').string
        num_comments = info_pad.find('span', {'class': 'comment'}).string
        num_loved = info_pad.find('span', {'class': 'loved'}).find('span').string
        if num_loved == '&bull;':
            num_loved = 0
        return title, uploader.rstrip(), int(num_comments), int(num_loved)

    def get_image_url(self):
        image_url = 'http:' + self._soup.find('div', {'class': 'img-wrap'}).find('img')['src']
        return image_url

    def get_share_num(self):
        num_fb_share = self._soup.find('a', {'class': 'facebook-share-button'}).string
        num_tweet = self._soup.find('a', {'class': 'twitter-tweet-button'}).string
        return int(num_fb_share), int(num_tweet)

    def get_fb_like_num(self):
        raw_fb_like_num = self._br.open("https://graph.facebook.com/fql?q=SELECT+total_count+FROM+link_stat+WHERE+url='%s'" % self._url)
        raw_fb_like_num = raw_fb_like_num.read()
        raw_fb_like_num = json.loads(raw_fb_like_num)
        return int(raw_fb_like_num['data'][0]['total_count'])

    def get_comments(self):
        raw_streams = self._br.open('https://graph.facebook.com/comments/?ids=%s&limit=1000' % self._url)
        raw_streams = raw_streams.read()
        raw_streams = json.loads(raw_streams)

        parsed_streams = []
        for raw_stream in raw_streams[self._url]['comments']['data']:
            parsed_stream = []
            parsed_stream.append({'cid': raw_stream['id'],
                                  'uid': raw_stream['from']['id'],
                                  'content': raw_stream['message'],
                                  'num_like': int(raw_stream['like_count'])
                                 })
            if 'comments' in raw_stream:
                for raw_reply in raw_stream['comments']['data']:
                    parsed_stream.append({'cid': raw_reply['id'],
                                          'uid': raw_reply['from']['id'],
                                          'content': raw_reply['message'],
                                          'num_like': -1
                                         })
            parsed_streams.append(parsed_stream)

        return parsed_streams



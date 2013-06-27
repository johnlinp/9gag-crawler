# -*- coding: utf-8 -*-

import re, json
import time
import xmllib
import mechanize
import cookielib
from BeautifulSoup import BeautifulSoup

class Browser:
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

    def _get_page_soup(self, url):
        okay = False
        while not okay:
            try:
                page = self._br.open(url)
                okay = True
            except:
                print 'sleep for mechanize error'
                time.sleep(60)
        content = page.read()
        content = re.sub('/ >', '/>', content) # workaround for strange BeautifulSoup...
        soup = BeautifulSoup(content)
        return soup

class HotPage(Browser):
    def __init__(self):
        Browser.__init__(self)
        self.reset()

    def reset(self):
        self._url = 'http://9gag.com/'
        self._gag_ids = []

    def next_gag_id(self):
        if not self._gag_ids:
            if not self._url:
                return None
            soup = self._get_page_soup(self._url)
            articles = soup.findAll('article')
            for article in articles:
                attrs = dict(article.attrs)
                if 'data-entry-id' in attrs:
                    self._gag_ids.append(attrs['data-entry-id'])
            assert self._gag_ids
            more = soup.find('a', {'class': 'next'})
            self._url = None if not more else 'http://9gag.com' + dict(more.attrs)['href']
        return self._gag_ids.pop(0)

class OneGag(Browser):
    OKAY = 'OKAY'
    ERROR = 'ERROR'

    IMAGE = 'IMAGE' # e.g. aOqqN8v
    VIDEO = 'VIDEO' # e.g. aeNNPrp
    GIF = 'GIF' # e.g. aPvvdyG
    NSFW = 'NSFW' # e.g. aXbb2Y9
    REMOVED = 'REMOVED' # e.g. 39203
    HTML_MALFORMED = 'HTML_MALFORMED'

    def open_gag(self, gag_id):
        url = 'http://9gag.com/gag/%s' % gag_id
        self._soup = self._get_page_soup(url)

        oops = self._soup.find('span', {'class': 'badge-toast-message'})
        if oops.string:
            return OneGag.ERROR, OneGag.REMOVED

        nsfw = self._soup.find('div', {'class': 'nsfw-post'})
        if nsfw:
            return OneGag.ERROR, OneGag.NSFW

        video = self._soup.find('div', {'class': 'badge-video-container'})
        if video:
            self._gag_type = OneGag.VIDEO
            return OneGag.OKAY, OneGag.VIDEO

        play = self._soup.find('span', {'class': 'play'})
        if play:
            self._gag_type = OneGag.GIF
            return OneGag.OKAY, OneGag.GIF

        self._gag_type = OneGag.IMAGE
        return OneGag.OKAY, OneGag.IMAGE

    def get_title(self):
        title = self._soup.find('section', {'id': 'individual-post'}) \
                          .find('article') \
                          .find('header') \
                          .find('h2') \
                          .string \
                          .strip()
        parser = xmllib.XMLParser()
        return parser.translate_references(title)

    def get_content_url(self):
        if self._gag_type == OneGag.IMAGE:
            content_url = self._soup.find('img', {'class': 'badge-item-img'})['src']
        elif self._gag_type == OneGag.GIF:
            content_url = self._soup.find('img', {'class': 'badge-item-animated-img'})['src']
        elif self._gag_type == OneGag.VIDEO:
            content_url = self._soup.find('iframe', {'class': 'video-element'})['src']
        else:
            content_url = ''
        return content_url

class Facebook(Browser):
    def _read_graph_api(self, url):
        okay = False
        while not okay:
            try:
                page = self._br.open(url)
                okay = True
            except:
                print 'sleep for facebook graph error'
                time.sleep(60)
        content = page.read()
        return json.loads(content)

    def _make_reply_dict(self, raw_block):
        return {'comment_id': raw_block['id'],
                'user_id': raw_block['from']['id'] if raw_block['from'] != None else '',
                'content': raw_block['message'],
                'num_like': int(raw_block['like_count']) if 'like_count' in raw_block else -1,
               }

    def get_comment_blocks(self, gag_id):
        url = 'http://9gag.com/gag/%s' % gag_id
        raw_blocks = self._read_graph_api('https://graph.facebook.com/comments/?ids=%s&limit=1000' % url)

        parsed_blocks = []
        for raw_block in raw_blocks[url]['comments']['data']:
            parsed_block = []
            parsed_block.append(self._make_reply_dict(raw_block))
            if 'comments' in raw_block:
                for raw_reply in raw_block['comments']['data']:
                    parsed_block.append(self._make_reply_dict(raw_reply))
            parsed_blocks.append(parsed_block)

        return parsed_blocks


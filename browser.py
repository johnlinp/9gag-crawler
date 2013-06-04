# -*- coding: utf-8 -*-

import re, json
import time
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
        content = re.sub('nsfw-post"', 'nsfw-post', content) # workaround for strange 9gag html...
        soup = BeautifulSoup(content)
        return soup

class HotPage(Browser):
    def __init__(self):
        Browser.__init__(self)
        self._url = 'http://9gag.com/'
        self._gag_ids = []

    def next_gag_id(self):
        if len(self._gag_ids) == 0:
            soup = self._get_page_soup(self._url)
            lis = soup.findAll('li')
            for li in lis:
                attrs = dict(li.attrs)
                if 'gagid' in attrs:
                    self._gag_ids.append(attrs['gagid'])
            more = soup.find('a', {'class': 'next'})
            if not more:
                return None
            self._url = 'http://9gag.com' + dict(more.attrs)['href']
            assert self._gag_ids
        return self._gag_ids.pop(0)

class OneGag(Browser):
    OKAY = 'OKAY'
    NSFW = 'NSFW'
    REMOVED = 'REMOVED'
    NOT_FOUND = 'NOT_FOUND'
    HTML_MALFORMED = 'HTML_MALFORMED'
    VIDEO = 'VIDEO'

    def open_gag(self, gag_id):
        url = 'http://9gag.com/gag/%s' % gag_id
        self._soup = self._get_page_soup(url)

        if self._soup.find('p', {'class': 'form-message error '}) is not None:
            return OneGag.REMOVED

        if self._soup.find('div', {'class': 'post-info-pad'}) is None:
            return OneGag.NSFW

        if self._soup.find('div', {'class': 'video-post'}) is not None:
            return OneGag.VIDEO

        return OneGag.OKAY

    def get_title(self):
        title = self._soup.find('div', {'class': 'post-info-pad'}) \
                          .find('h1') \
                          .string
        return unicode(title.rstrip())

    def get_uploader(self):
        links = self._soup.findAll('a', {'target': '_blank'});
        for link in links:
            attrs = dict(link.attrs)
            if 'href' in attrs:
                mo = re.search('http://9gag.com/u/(\w+)', attrs['href'])
                if mo:
                    return mo.group(1)
        return ''

    def get_content_url(self):
        content_url = 'http:' + self._soup.find('div', {'class': 'img-wrap'}).find('img')['src']
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


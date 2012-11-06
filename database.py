# -*- coding: utf-8 -*-

import re
import pg

class Database:
    def __init__(self):
        self.conn = pg.connect('ninegag', 'gardenia.csie.ntu.edu.tw', 5432, None, None, 'ninegag', 'agent#336')

    def add_slashes(self, string):
        return re.sub("'", "\\\\'", string)

    def insert_gag(self, gid, uploader, title, image_url, num_comments, num_loved, num_fb_share, num_fb_like, num_tweet):
        uploader = self.add_slashes(uploader)
        title = self.add_slashes(title)
        self.conn.query('''INSERT INTO gag (
                               gid, uploader, title, image_url, num_comments, num_loved, num_fb_share, num_fb_like, num_tweet
                           ) 
                           VALUES (
                               %d, E'%s', E'%s', E'%s', %d, %d, %d, %d, %d
                           )'''
                           % (gid, uploader, title, image_url, num_comments, num_loved, num_fb_share, num_fb_like, num_tweet)
        )

    def err_gag(self, gid, err_msg):
        self.insert_gag(gid, err_msg, '', '', 0, 0, 0, 0, 0)

    def last_gag_id(self):
        query = self.conn.query('SELECT COUNT(*) FROM gag')
        res = query.getresult()
        if res[0][0] == 0:
            return 0
        query = self.conn.query('SELECT MAX(gid) FROM gag')
        res = query.getresult()
        return res[0][0]

    def insert_comment(self, gid, sid, cid, username, is_top_commenter, content, num_like):
        username = self.add_slashes(username)
        content = self.add_slashes(content)
        self.conn.query('''INSERT INTO comment (
                               gid, sid, cid, username, is_top_commenter, content, num_like
                           ) 
                           VALUES (
                               %d, %d, %d, E'%s', %d, E'%s', %d
                           )'''
                           % (gid, sid, cid, username, is_top_commenter, content, num_like)
        )


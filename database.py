# -*- coding: utf-8 -*-

import pg

class Database:
    def __init__(self):
        self.conn = pg.connect('ninegag', 'gardenia.csie.ntu.edu.tw', 5432, None, None, 'ninegag', 'agent#336')

    def insert_gag(self, gid, title, image_url, num_comments, num_loved, num_fb_share, num_fb_like, num_tweet):
        self.conn.query('''INSERT INTO gag (
                             gid, title, image_url, num_comments, num_loved, num_fb_share, num_fb_like, num_tweet
                         ) 
                         VALUES (
                             %d, '%s', '%s', %d, %d, %d, %d, %d
                         )'''
                         % (gid, title, image_url, num_comments, num_loved, num_fb_share, num_fb_like, num_tweet)
        )

    def err_gag(self, gid, err_msg):
        self.insert_gag(gid, err_msg, '', 0, 0, 0, 0, 0)

    def last_gag_id(self):
        query = self.conn.query('SELECT MAX(gid) FROM gag')
        res = query.getresult()
        return res[0][0]

# -*- coding: utf-8 -*-

import re
import time
import pg

class Database:
    def __init__(self):
        self.conn = pg.connect('ninecrawl', 'gardenia.csie.ntu.edu.tw', 5432, None, None, 'ninegag', 'agent#336')

    def _add_slashes(self, string):
        string = string.encode('utf8')
        string = re.sub("\\\\", "\\\\\\\\", string)
        string = re.sub("'", "\\\\'", string)
        return string

    def delete_comment(self, gag_id):
        self.conn.query("DELETE FROM comment WHERE gag_id = '%s'" % gag_id)

    def have_gag(self, gag_id):
        query = self.conn.query("SELECT COUNT(*) FROM gag WHERE gag_id = '%s'" % gag_id)
        res = query.getresult()
        return res[0][0] != 0

    def insert_gag(self, gag_id, title, uploader, content_url):
        title = self._add_slashes(title)
        uploader = self._add_slashes(uploader)
        content_url = self._add_slashes(content_url)
        okay = False
        while not okay:
            try:
                query_cmd = """INSERT INTO gag (
                                   gag_id, title, uploader, content_url
                               ) 
                               VALUES (
                                   E'%s', E'%s', E'%s', E'%s'
                               )""" % (gag_id, title, uploader, content_url)
                okay = True
            except:
                print 'insert_gag error'
                print gag_id, title, uploader, content_url
                time.sleep(60)
        self.conn.query(query_cmd)

    def err_gag(self, gag_id, err_msg):
        self.insert_gag(gag_id, err_msg, '', '')

    def last_gag_id(self):
        query = self.conn.query('SELECT COUNT(*) FROM gag')
        res = query.getresult()
        if res[0][0] == 0:
            return 0
        query = self.conn.query('SELECT MAX(gag_id) FROM gag')
        res = query.getresult()
        return res[0][0]

    def insert_comment(self, gag_id, block_id, reply_id, comment_id, user_id, content, num_like):
        gag_id = self._add_slashes(gag_id)
        comment_id = self._add_slashes(comment_id)
        user_id = self._add_slashes(user_id)
        content = self._add_slashes(content)
        try:
            query_cmd = """INSERT INTO comment (
                               gag_id, block_id, reply_id, fb_comment_id, fb_user_id, content, num_like
                           ) 
                           VALUES (
                               E'%s', %d, %d, E'%s', E'%s', E'%s', %d
                           )""" % (gag_id, block_id, reply_id, comment_id, user_id, content, num_like)
        except:
            print 'insert_comment error'
            print gag_id, block_id, reply_id, comment_id, user_id, content, num_like
            raise
        self.conn.query(query_cmd)


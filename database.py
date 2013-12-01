# -*- coding: utf-8 -*-

import re
from datetime import datetime
import time
import psycopg2

class Database:
    def __init__(self):
        self._conn = psycopg2.connect(database='ninecrawl', host='gardenia.csie.ntu.edu.tw', user='ninegag', password='agent#336')
        self._cursor = self._conn.cursor()

    def _add_slashes(self, string):
        string = string.encode('utf8')
        string = re.sub(r"\\", r"\\\\", string)
        string = re.sub("'", r"\\'", string)
        return string

    def delete_gag(self, gag_id):
        self._cursor.execute("DELETE FROM gag WHERE gag_id = '%s'" % gag_id)
        self._conn.commit()

    def delete_comment(self, gag_id):
        self._cursor.execute("DELETE FROM comment WHERE gag_id = '%s'" % gag_id)
        self._conn.commit()

    def have_gag(self, gag_id):
        self._cursor.execute("SELECT COUNT(*) FROM gag WHERE gag_id = '%s'" % gag_id)
        res = self._cursor.fetchall()
        return res[0][0] != 0

    def insert_gag(self, gag_id, typee, title, uploader, content_url, publish_time, crawl_time, ago):
        title = self._add_slashes(title)
        uploader = self._add_slashes(uploader)
        content_url = self._add_slashes(content_url)
        self._cursor.execute("""INSERT INTO gag (
                                    gag_id, type,
                                    title, uploader, content_url,
                                    publish_time, crawl_time, ago
                                )
                                VALUES (
                                    %s, %s,
                                    %s, %s, %s,
                                    %s, %s, %s
                                )""", (
                                    gag_id, typee[:2],
                                    title, uploader, content_url,
                                    publish_time, crawl_time, ago
                                )
                            )
        self._conn.commit()

    def err_gag(self, gag_id):
        self.delete_gag(gag_id)
        query_cmd = "INSERT INTO gag (gag_id, crawl_time) VALUES (E'%s', '%s')" % (gag_id, datetime.now())
        self._cursor.execute(query_cmd)
        self._conn.commit()

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
        self._cursor.execute(query_cmd)
        self._conn.commit()


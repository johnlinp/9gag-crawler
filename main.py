# -*- coding: utf-8 -*-

import os, re
from browser import Browser
from database import Database

def main():
    br = Browser()
    db = Database()

    begin = db.last_gag_id() + 1
    begin = 5777375
    for gid in range(begin, 9999999):
        status = br.open_gag(gid)
        print status
        if status != Browser.OKAY:
            db.err_gag(gid, status)
            continue

        title, uploader, num_comments, num_loved = br.get_info_pad()
        image_url = br.get_image_url()
        num_fb_share, num_tweet = br.get_share_num()
        num_fb_like = br.get_fb_like_num()
        db.insert_gag(gid, uploader, title, image_url, num_comments, num_loved, num_fb_share, num_fb_like, num_tweet)

        streams = br.get_comments()
        for sid, stream in enumerate(streams):
            for cid, comment in enumerate(stream):
                db.insert_comment(gid, sid, cid, comment[0], comment[1], comment[2], comment[3])
        break

if __name__ == '__main__':
    main()


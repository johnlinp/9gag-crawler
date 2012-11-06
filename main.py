# -*- coding: utf-8 -*-

import os, re
from browser import Browser
from database import Database

def main():
    br = Browser()
    db = Database()

    begin = db.last_gag_id() + 1
    begin = 5750473
    for gid in range(begin, 9999999):
        br.open_gag(gid)
        status = br.get_status()
        print status
        if status != Browser.OKAY:
            db.err_gag(gid, status)
            continue

        title, uploader, num_comments, num_loved = br.get_info_pad()
        image_url = br.get_image_url()
        num_fb_share, num_fb_like, num_tweet = br.get_external_num()
        db.insert_gag(gid, uploader, title, image_url, num_comments, num_loved, num_fb_share, num_fb_like, num_tweet)

        streams = br.get_comments()
        for sid, stream in enumerate(streams):
            for cid, comment in enumerate(stream):
                db.insert_comment(gid, sid, cid, comment[0], comment[1], comment[2], comment[3])
        break

if __name__ == '__main__':
    main()


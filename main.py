# -*- coding: utf-8 -*-

import os, re
from browser import Browser
from database import Database

def main():
    br = Browser()
    db = Database()

    begin = db.last_gag_id()
    db.delete_info(begin)

    for gid in range(begin, 9999999):
        status = br.open_gag(gid)
        print gid, status
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
            for rid, reply in enumerate(stream):
                db.insert_comment(gid, sid, rid, reply['cid'], reply['uid'], reply['content'], reply['num_like'])

if __name__ == '__main__':
    main()


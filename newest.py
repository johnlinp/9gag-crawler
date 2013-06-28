# -*- coding: utf-8 -*-

import os, re
from datetime import datetime
import time
from browser import HotPage, OneGag, Facebook
from database import Database

def main():
    hot = HotPage()
    one = OneGag()
    fb = Facebook()
    db = Database()

    prev_gag_id = None
    while True:
        hot.reset()
        cur_gag_id = hot.next_gag_id()
        if cur_gag_id == prev_gag_id:
            print 'sleep...'
            time.sleep(60)
            continue
        print cur_gag_id,

        if db.have_gag(cur_gag_id):
            print 'skip',
        else:
            status, typee = one.open_gag(cur_gag_id)
            print status, typee,

            if status != OneGag.OKAY:
                db.err_gag(cur_gag_id, status, typee)
                print
                continue

            title = one.get_title()
            uploader = one.get_uploader()
            content_url = one.get_content_url()
            publish_time = one.get_post_time()
            crawl_time = datetime.now()
            ago = one.get_ago()
            print 'insert', 
            db.insert_gag(cur_gag_id, status, typee, title, uploader, content_url, publish_time, crawl_time, ago)

        print 'getting comments...',
        db.delete_comment(cur_gag_id)
        blocks = fb.get_comment_blocks(cur_gag_id)
        for block_id, block in enumerate(blocks):
            for reply_id, reply in enumerate(block):
                db.insert_comment(cur_gag_id,
                                  block_id, reply_id, 
                                  reply['comment_id'], reply['user_id'], reply['content'], reply['num_like'])
        print 'done'
        prev_gag_id = cur_gag_id

if __name__ == '__main__':
    main()


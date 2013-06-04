# -*- coding: utf-8 -*-

import os, re
from browser import HotPage, OneGag, Facebook
from database import Database

def main():
    hot = HotPage()
    one = OneGag()
    fb = Facebook()
    db = Database()

    while True:
        gag_id = hot.next_gag_id()
        if gag_id == None:
            print 'Reach the limit of old Hot Page'
            exit()
        print gag_id,

        if db.have_gag(gag_id):
            print 'skip',
        else:
            status = one.open_gag(gag_id)
            print status,

            if status != OneGag.OKAY:
                db.err_gag(gag_id, status)
                print
                continue

            title = one.get_title()
            uploader = one.get_uploader()
            content_url = one.get_content_url()
            db.insert_gag(gag_id, title, uploader, content_url)

        print 'getting comments...',
        db.delete_comment(gag_id)
        blocks = fb.get_comment_blocks(gag_id)
        for block_id, block in enumerate(blocks):
            for reply_id, reply in enumerate(block):
                db.insert_comment(gag_id,
                                  block_id, reply_id, 
                                  reply['comment_id'], reply['user_id'], reply['content'], reply['num_like'])
        print 'done'

if __name__ == '__main__':
    main()


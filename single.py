# -*- coding: utf-8 -*-

import sys, re
from datetime import datetime
import time
from browser import HotPage, OneGag, Facebook
from database import Database

def main(argv):
    if len(argv) != 2:
        print 'usage:'
        print '    python single.py gag_id'
        exit()

    gag_id = argv[1]

    one = OneGag()
    fb = Facebook()
    db = Database()

    if db.have_gag(gag_id):
        print 'skip',
        sys.stdout.flush()
    else:
        status, typee = one.open_gag(gag_id)
        print status, typee,
        sys.stdout.flush()

        if status != OneGag.OKAY:
            db.err_gag(gag_id, status, typee)
            print

        title = one.get_title()
        uploader = one.get_uploader()
        content_url = one.get_content_url()
        crawl_time = datetime.now()
        print 'insert', 
        sys.stdout.flush()
        db.insert_gag(gag_id, typee, title, uploader, content_url, None, crawl_time, None)

    print 'getting comments...',
    sys.stdout.flush()
    db.delete_comment(gag_id)
    blocks = fb.get_comment_blocks(gag_id)
    for block_id, block in enumerate(blocks):
        for reply_id, reply in enumerate(block):
            db.insert_comment(gag_id,
                              block_id, reply_id, 
                              reply['comment_id'], reply['user_id'], reply['content'], reply['num_like'])
    print 'done'

if __name__ == '__main__':
    main(sys.argv)


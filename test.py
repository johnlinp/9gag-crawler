from datetime import datetime
import sys

def test_gag_type():
    from browser import OneGag

    cases = {
        'aOqqN8v': ('OKAY', 'IMAGE'),
        'aeNNPrp': ('OKAY', 'VIDEO'),
        'aPvvdyG': ('OKAY', 'GIF'),
        'aXbb2Y9': ('ERROR', 'NSFW'),
        '39203': ('ERROR', 'REMOVED'),
    }

    one = OneGag()
    for gag_id, answer in cases.items():
        print gag_id, answer,
        guess = one.open_gag(gag_id)
        if guess != answer:
            print ' -> %s' % (guess,) 
            exit()
        print 'correct'

def test_gag_info():
    from browser import OneGag

    cases = [
        (
            'aLKKVeW',
            {
                'title': "Steroids vs. Photoshop",
                'content_url': 'http://d3dsacqprgcsqh.cloudfront.net/photo/aLKKVeW_700b_v2.jpg',
                'uploader': 'ons3t',
            }
        ),
        (
            'av004Kd',
            {
                'title': "How students feel every year on the last day of school",
                'content_url': 'http://d3dsacqprgcsqh.cloudfront.net/photo/av004Kd_700b.jpg',
                'uploader': 'godfishcute',
            }
        ),
        (
            'aOqqN8v',
            {
                'title': "Something we're all guilty of.",
                'content_url': 'http://d3dsacqprgcsqh.cloudfront.net/photo/aOqqN8v_700b.jpg',
                'uploader': '',
            }
        ),
        (
            'aeNNPrp',
            {
                'title': "Korean artist Kim Jung Gi - Awesome demonstration of drawing!",
                'content_url': 'http://www.youtube.com/embed/3oQEPB0Lus4?showinfo=0&autohide=1&autoplay=1&iv_load_policy=3',
                'uploader': '',
            }
        ),
        (
            'aPvvdyG',
            {
                'title': "Where does the 2nd ref come from??",
                'content_url': 'http://d3dsacqprgcsqh.cloudfront.net/photo/aPvvdyG_460sa.gif',
                'uploader': '',
            }
        ),
    ]

    one = OneGag()
    for gag_id, answer in cases:
        print gag_id,
        status, gag_type = one.open_gag(gag_id)

        title = one.get_title()
        if title != answer['title']:
            print '"%s" != "%s"' % (title, answer['title'])
            exit()

        content_url = one.get_content_url()
        if content_url != answer['content_url']:
            print '"%s" != "%s"' % (content_url, answer['content_url'])
            exit()

        uploader = one.get_uploader()
        if uploader != answer['uploader']:
            print '"%s" != "%s"' % (uploader, answer['uploader'])
            exit()

        print 'correct'

def main(argv):
    if len(argv) != 2:
        print 'usage:'
        print '    python test.py which'
        exit()

    which = argv[1]
    tests = {
        'type': test_gag_type,
        'info': test_gag_info
    }

    if which in tests:
        tests[which]()
    else:
        print 'candidates are:'
        print '    ' + ', '.join(tests.keys())
        exit()

if __name__ == '__main__':
    main(sys.argv)


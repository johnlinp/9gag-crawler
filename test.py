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
            break
        print 'correct'

def main(argv):
    if len(argv) != 2:
        print 'usage:'
        print '    python test.py which'
        exit()

    which = argv[1]
    tests = {
        'type': test_gag_type,
    }

    if which in tests:
        tests[which]()
    else:
        print 'candidates are:'
        print '    ' + ', '.join(tests.keys())
        exit()

if __name__ == '__main__':
    main(sys.argv)


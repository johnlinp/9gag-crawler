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

#!/usr/bin/env python2.7

import os, sys, re

def ispng(filename):
    fn, ext = os.path.splitext(filename)
    if ext.lower() == ".png":
        return True

def common(s1, s2):
# TODO - there's probably a nicer way to do this, not that it's time critical
    s = ''
    for a, b in zip(s1, s2):
        if a != b:
            break
        else:
            s += a
    return s

def sorted_nicely( l ): 
    """ Sort the given iterable in the way that humans expect.""" 
    convert = lambda text: int(text) if text.isdigit() else text 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)

def get_stack_pattern(stackdir):

    dirlist = os.listdir(stackdir)

    pl = sorted_nicely([f for f in dirlist if ispng(f)])

    print pl

    print pl[0], pl[-1]

    imprefix = common(pl[0], pl[-1])
    il = len(imprefix)
    istart = pl[0][il:-4]
    iend = pl[-1][il:-4]

    ld = len(iend)

    return os.path.join(stackdir, imprefix + '%0' + str(ld) + 'd.png'), int(istart), int(iend)

def main():
    try:
        stackdir = sys.argv[1]
    except IndexError:
        print "Please supply stack dir"
        sys.exit(1)

    print get_stack_pattern(stackdir)

if __name__ == '__main__':
    main()

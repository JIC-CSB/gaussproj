#!/usr/bin/env python2.7

import os, sys

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

def get_stack_pattern(stackdir):

    dirlist = os.listdir(stackdir)

    pl = sorted([f for f in dirlist if ispng(f)])

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

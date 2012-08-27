#!/usr/bin/env python2.7
import os
import subprocess

for sdr in range(0, 50, 2):
    for sdz in range(0, 20, 2):
        bcommand = [    'echo',
                '-o',  '"$HOME/projects/yaraproj/output/stdout/out-%J.txt"',
                ' ./src/gaussproj.py', str(sdr), str(sdr), str(sdz)]

        p = subprocess.call(bcommand)

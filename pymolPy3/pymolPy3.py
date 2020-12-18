#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE

class pymolPy3:
    def __init__(self, mode = 1):
        # Enable gui...
        cmd = 'pymol -p'

        # Turn off gui...
        if mode != 1: cmd = 'pymol -pc'

        # Create a subprocess...
        self.pymolpy3 = Popen(cmd, shell=True, stdin=PIPE)

    def __del__(self):
        # Turn off stdin...
        self.pymolpy3.stdin.close()

        # Wait until program is over...
        self.pymolpy3.wait()

        # Terminate the subprcess...
        self.pymolpy3.terminate()

    def __call__(self, s):
        # Keep reading the new pymol command as a byte string...
        self.pymolpy3.stdin.write( bytes( (s + '\n').encode() ) )

        # Flush it asap...
        self.pymolpy3.stdin.flush()

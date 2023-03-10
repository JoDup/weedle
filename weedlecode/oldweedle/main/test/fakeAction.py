#!/usr/bin/env python

import os
import sys

arguments = list(sys.argv)
arguments.pop(0)
print "Executing %s with arguments %s" % (os.path.abspath(__file__), str(arguments))

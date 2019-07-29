#!/usr/bin/env python3

import howler_bits
import glob
import os

for file in glob.glob("test/*.mp3"):
        os.system("./howler_bits.py" + ' ' + file)

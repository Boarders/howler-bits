#!/usr/bin/env python3

from pydub import AudioSegment
from helpers import *
import os
import sys

def main():
    cl_inputs = sys.argv[1:]
    if (len(cl_inputs) == 0):
        sys.exit ("No input files provided!")
    else:
        for file_name in cl_inputs:
            dir_name = os.path.dirname(file_name)
            ext = os.path.splitext(file_name)[1][1:]
            audio = AudioSegment.from_file(file_name, ext)
            name = os.path.basename(file_name)
            output_dir = os.path.join (dir_name, 'output')

            if not os.path.exists(output_dir):
                os.mkdir(output_dir)
            split_and_output_audio(audio, ext, name, file_name, output_dir)


if __name__ == "__main__":
    main()



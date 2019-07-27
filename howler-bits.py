from pydub import AudioSegment
from helpers import *
import os
import sys

audio_dir = 'TODO'
file_name = "room4.mp3"
# remove the directory
base_name = os.path.basename(file_name)
# split the name and file extension)
(name, extension) = (os.path.splitext(file_name))

audio = AudioSegment.from_mp3(base_name)

def main_transformation():
    (seg1, seg2, seg3, third) = split_in_three(audio)
    segs1 = split_audio_and_make_name (five_min, seg1, name, 0)
    segs2 = split_audio_and_make_name (ten_min,  seg2, name, third)
    segs3 = split_audio_and_make_name (fifteen_min, seg2, name, 2 * third)

    output_all(segs1)
    output_all(segs2)
    output_all(segs3)

main_transformation()


def split_file(file_name):
    base_name = os.path.basename(file_name)
    audio = Audio.Segment.from_mp3(file_name)
    ext = os.path.splitext(file_name)


from pydub import AudioSegment
from functools import partial
from math import floor
import os

# units of time in milliseconds
sec = 1000
minute = 60 * sec
five_min = 5 * minute
ten_min = 10 * minute
fifteen_min = 15 * minute

def get_time(milliseconds):
    total_seconds     = int(milliseconds / 1000)
    total_minutes     = total_seconds // 60
    total_hours       = total_minutes // 60
    remaining_minutes = total_minutes % 60
    remaining_seconds = total_seconds % 60
    return (total_hours, remaining_minutes, remaining_seconds)

def format_time_string (h, m, s):
    if (h == 0 and m == 0 and s == 0):
        return "start"
    elif h == 0:
        return "{}m{}s".format(m, s)
    else:
        return "{}h{}m{}s".format(h, m, s)

def format_time (ms):
    (h, m, s) = get_time(ms)
    return format_time_string(h, m, s)
    

# This function takes the input name and constructs the new name
def make_file_name(current_file_name, start_time, end_time):
 #   def file_name_transform(file_name):
 #       return file_name
    s = "{} ({}-{})".format(current_file_name, format_time(start_time), format_time(end_time))
    return s


# This function splits the audio into segments returning a list
# containing a tuple of the audio segment along the name of the segment
def split_audio_and_make_name(segment_length : int, audio, name, start, output_dir):
    audio_end = len(audio) + start
    # This is the number of segments we will have
    num_segments = int(floor(len(audio) / segment_length))
    # This is the last integer segment_length in the clip
    last_segment_point = int(num_segments * segment_length)
    
    l = [ ( audio[t * (segment_length) : (t + 1) * segment_length]
          , make_file_name
              ( name
              , start + t * (segment_length)
              , min (start + (t + 1) * (segment_length), audio_end))
          , output_dir
          ) for t
          in range(0 , num_segments + 1)
        ]
    return l
    
# split the audio in three returning a tuple of each third and the length of a third
# in time units compatible with Pydub.
def split_in_three(audio):
    l = len(audio)
    third = l / 3
    two_thirds = third + third
    return (audio[0:third], audio[third: two_thirds], audio [two_thirds:], third)
    

# Write audio with a given extension to the output directory.
def output_file(extension, audio, name, output_dir):
    filename = name + "." + extension
    output_file_path = os.path.join (output_dir, filename)
    with open(output_file_path, "wb") as f:
        audio.export(f,format = extension)


# Output audio produced by split_and_make_name.
def output_all(ext, ls):
    for p in ls:
        output_file(ext,p[0], p[1], p[2])

# split up audio into three parts and output it as the given file type.
def split_and_output_audio(audio, ext, name, file_name, output_dir):
    (seg1, seg2, seg3, third) = split_in_three(audio)
    segs1 = split_audio_and_make_name (five_min, seg1, name, 0, output_dir)
    segs2 = split_audio_and_make_name (ten_min,  seg2, name, third, output_dir)
    segs3 = split_audio_and_make_name (fifteen_min, seg2, name, 2 * third, output_dir)

    output_all(ext, segs1)
    output_all(ext, segs2)
    output_all(ext, segs3)        

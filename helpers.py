from pydub import AudioSegment
from functools import partial
from math import floor


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
def split_audio_and_make_name(segment_length : int, audio, name, start):
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
          ) for t
          in range(0 , num_segments + 1)
        ]
    return l
    

def split_in_three(audio):
    l = len(audio)
    third = l / 3
    two_thirds = third + third
    return (audio[0:third], audio[third: two_thirds], audio [two_thirds:], third)
    

def output_file(extension, audio, name):
    filename = name + "." + extension
    with open("output/" + filename, "wb") as f:
        audio.export(f,format = extension)


output_mp3 = partial(output_file, 'mp3')

def output_all(ls):
    for p in ls:
        output_mp3(p[0], p[1])
  


#to do:
# - error with naming after split into three
#   e.g. if segment is not multiple of five minutes then the end time is incorrect


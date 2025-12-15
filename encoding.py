import os
import sys
# pip install ffmpeg-python
# not just 'ffmpeg' --> may not work!
import ffmpeg

### SOURCES ###
# https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory #
# https://medium.com/@aleksej.gudkov/ffmpeg-python-example-a-guide-to-using-ffmpeg-with-python-020cdb7733e7 #
# https://trac.ffmpeg.org/wiki/Encode/AV1 #


# get all files from the path --> test sequences
def get_files(path):
    videos = []
    for entry in os.scandir(path):
        if entry.is_file():
            videos.append(entry.path)
    return videos


# retrieve file name from path, so output can be named the same --> also remove extension!
def get_filename(file_name):
    return file_name.split('\\')[-1].split('.')[-2]

# encode the video with AV1 --> keep initial config (resolution, bitrate, etc.)
def encode_av1(video):
    input = video
    output = f'./av1_sequences\\\{get_filename(input)}.mp4'
    print(output)
    try:
        ffmpeg.input(input).output(output, vcodec='libsvtav1').run()
    except ffmpeg.Error as e:
        print(f"An error occurred: {e}")

# encode all videos with AV1 --> keep initial config (resolution, bitrate, etc.)
def encode_av1_all(videos):
    for video in videos:
       encode_av1(video)


if __name__ == "__main__":
    TEST_SEQ_DIR = './test_sequences'
    if len(sys.argv) == 2:
        #sys.argv[0] is the program name
        #sys.argv[1] is the 1st argument --> here: video name (in case we want to encode single video)
        encode_av1(TEST_SEQ_DIR + '\\'+ sys.argv[1])
    elif len(sys.argv) > 2:
        print(f"Too many arguments. \nUsage: python {sys.argv[0]} <video name>. \nIf omitted, all videos will be encoded.")
    else:
        videos = get_files(TEST_SEQ_DIR)
        encode_av1_all(videos)

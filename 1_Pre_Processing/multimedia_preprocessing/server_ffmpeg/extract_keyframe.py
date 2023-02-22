import sys
sys.path.insert(0, './utils/')
from utils.util import check_filename, check_dir

import os
import argparse

def parse_args():
    """ configuration arguments only for files in the current dir
    
    Args:
    """
    parser = argparse.ArgumentParser()
    # common
    parser.add_argument("video_dir", default="", type=str) 
    parser.add_argument("image_dir", default="", type=str)

    args = parser.parse_args()
    return args

def extract_keyframe(video_dir, output_dir):
    """ extract key frames of video by the ffmpeg
    
    Args:
        video_dir (str): the dir of video
        output_dir (str): the dir of output keyframe
    """
    for video in os.listdir(video_dir):
        # if there are some spaces in the video name, then replace with _
        suffix = os.path.splitext(video)[-1]
        if suffix not in [".mp4"]:
            continue
        video_ = video.split(" ")
        video_new = "_".join(video_)
        video_new = check_filename(video_new)
        os.rename(os.path.join(video_dir, video), os.path.join(video_dir, video_new)) # rename video 
        # read video prop
        video_path = os.path.join(video_dir, video_new)
        if os.path.isfile(video_path):
            portion = os.path.splitext(video_new) # file name and extension
            # first extract key frames to save into images
            image_dir = os.path.join(output_dir, portion[0])
            check_dir(image_dir) # if not exist image dir, then create it
            os.system("ffmpeg -i {} -vf select='eq(pict_type\,I)' -vsync 2 -ss 0 -f image2 {}".format(video_path, os.path.join(image_dir, "%6d.jpg")))
            # second extract the index of key frames from the video by ffprobe
            os.system("ffprobe -select_streams v -show_frames -show_entries frame=pict_type -of csv {} | grep -n I | cut -d ':' -f 1 > {}".format(video_path, os.path.join(image_dir, "frame_indices.txt")))

if __name__ == "__main__":
    #args = parse_args()
    #extract_keyframe(args.video_dir, args.image_dir)
    #for Q7 run
    video_dir="/usr0/home/zhiqic/chronos-ta1/corpus/q7-data/data/mp4"
    image_dir="/usr0/home/zhiqic/chronos-ta1/corpus/q7-data/videos"
    extract_keyframe(video_dir, image_dir) 
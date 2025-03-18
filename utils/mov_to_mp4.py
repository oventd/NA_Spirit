# Convert the video to mp4 format\
import moviepy
import os
path = "/nas/spirit/DB/turnaround"
videos = os.listdir(path)

for video in videos:
    video_name = os.path.join(path, video)
    clip = moviepy.VideoFileClip(video_name)
    video_name, ext = os.path.splitext(video_name)
    mp4_video_name = f"{video_name}.mp4"
    print(mp4_video_name)
    clip.write_videofile(mp4_video_name)

    # Remove the original AVI file
    # os.remove(video_name)
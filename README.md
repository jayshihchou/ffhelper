# ffmpeg_helper

## Requirement:

  ffmpeg, python3

## Usage:
#### dummper
  python dumpper.py -i video.mp4 -o ./result --dump_image

#### cat_video
  python cat_video.py -i1 video1.mp4 -i2 video2.mp4 -c1 256:256:0:0 -c2 256:256:0:0 -m 1,1+2*0.5,2

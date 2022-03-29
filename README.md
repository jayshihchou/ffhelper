# ffhelper

## Requirement
```
ffmpeg, python 3.6 or higher
```
## Usage
### Dump Datas
#### Dump images
```
python -m ffhelper dump -i video.mp4 -o ./result --dump_image --fps 30
```
#### Dump audio
```
python -m ffhelper dump -i video.mp4 -o ./result/video.aac --dump_audio
```
#### Dump metadata
```
python -m ffhelper dump -i video.mp4 -o dump/metadata.txt --dump_meta
```
### Replace audio to a video
```
python -m ffhelper dump -i video.mp4 -o results/video.mp4 -ia audio.aac --replace_audio
```

### Images to video
```
python -m ffhelper im2vid -i path/to/images --fps 30 --o output.mp4
```

### Append videos
Append video2 at end of video1.
```
python -m ffhelper join -i1 video1.mp4 -i2 video2.mp4 -o output.mp4 --no_audio
```

### Combine videos
Crop both video into 256x256 and combine into one video. (video length is longer one, and shorter one will use last frame)
```
                   # --input1 is first video, --input2 is second video ... until --input16
                   #                              --cropx: format width:height:startX:startY
                   #                                                              --map: ',' means end of this part
                   #                                                                  number is correspond to -i{number}
                   #                                                                  in this case will generate 512x256 video and order is 1,2.
python -m ffhelper combine -i1 video1.mp4 -i2 video2.mp4 -c1 256:256:0:0 -c2 256:256:0:0 -m 1,2 -o output.mp4
```
Crop and resize both video into 512x512 and combine into one video.
```
                                                                                # --scalex format width:height
python -m ffhelper combine -i1 video1.mp4 -i2 video2.mp4 -c1 256:256:0:0 -c2 256:256:0:0 -s1 512:512 -s2 512:512 -m 1,2 -o output.mp4
```
Add blend video between video1 and video2 (with same crop as above):
```
                                                                                 # 1+2 means there are 1 and 2 video in same part
                                                                                 # and 1 is background video,
                                                                                 # 2*0.5 means 2's alpha is 0.5
python -m ffhelper combine -i1 video1.mp4 -i2 video2.mp4 -c1 256:256:0:0 -c2 256:256:0:0 -m 1,1+2*0.5,2 -o output.mp4
```

### Add text to video
```
                              # -b: add background -ba: background alpha(float)
                              #            -s: font size  -c: font color -f: font name
                              #                                    -t{n}: number n's text
                              #                                                  -p{n}: number n's text position format: x=???:y=???
                              #                                                         main_h = main video height (also main_w)
                              #                                                         text_h = text height (also text_w)
python -m ffhelper add_text -i input.mp4 -b -ba 0.5 -s 24 -c white -f Arial -t1 left_text -p1 x=10:y=main_h-text_h-10 -t2 right_text -p2 x=main_w-text_w-10:y=main_h-text_h-10 -o output.mp4
```

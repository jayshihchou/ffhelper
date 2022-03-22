import argparse
import os


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, help='input video file', required=True)
    parser.add_argument('-ia', '--input_audio', type=str, help='input audio file')
    parser.add_argument('-o', '--output', type=str, help='output folder (default is ./results/)', default='./results/')
    parser.add_argument('-di', '--dump_image', help=(
        'dump image mode usage: '
        'python dumpper.py -i video.mp4 -o dump/images/ --dump_image'
    ), action='store_true')
    parser.add_argument('-da', '--dump_audio', help=(
        'dump audio mode usage: '
        'python dumpper.py -i video.mp4 -o dump/audio.aac --dump_audio'
    ), action='store_true')
    parser.add_argument('-dm', '--dump_meta', help=(
        'dump metadata mode usage: '
        'python dumpper.py -i video.mp4 -o dump/metadata.txt --dump_meta'
    ), action='store_true')
    parser.add_argument('-ra', '--replace_audio', help=(
        'replace video audio from input audio file usage: '
        'python dumpper.py -i video.mp4 -o results/video.mp4 -ia audio.aac --replace_audio'
    ), action='store_true')
    parser.add_argument('-f', '--fps', type=int, help='fps rate (-1 to use default)', default=-1)
    parser.add_argument('-q', '--dump_quality', type=int, help=(
        'dump quality for jpg (normal range is 2-31 31 is worst)'), default=2)
    return parser.parse_args()


def main():
    args = parse_args()
    cmd = f'ffmpeg -i {args.input}'
    if args.input_audio is not None:
        cmd += f' -i {args.input_audio}'

    fps = args.fps

    output = args.output.lower()
    if args.dump_image:
        print('dump image...')
        os.makedirs(output, exist_ok=True)
        if not ('.png' in output or '.jpg' in output or '.jpeg' in output):
            output = os.path.join(output, '%05d.jpg')
        output = f' {output}'
        if args.dump_quality > 0:
            output = f' -q:v {args.dump_quality} {output}'
        if fps > 0:
            output = f' -vf "fps={fps}"{output}'
    elif args.dump_audio:
        print('dump audio...')
        output = f' -vn -acodec copy {output}'
    elif args.dump_meta:
        print('dump meta...')
        output = f' -f ffmetadata {output}'
    elif args.replace_audio:
        print('dump replace audio...')
        output = f' -map 0:v -map 1:a -c:v copy -shortest {output}'
    else:
        print('nothing to do')
        exit()
    cmd += output

    print(f'========= dumpper run: {cmd}')
    os.system(cmd)
    print(f'========= dumpper done: {cmd}')


if __name__ == '__main__':
    main()
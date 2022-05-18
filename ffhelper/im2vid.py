import argparse
import glob
import os
from pathlib import Path
from typing import List


def parse_args(additional: bool = False) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    if additional:
        parser.add_argument('COMMAND', help='command to use')
    parser.add_argument('-i', '--input', type=str, help='input image path', required=True)
    parser.add_argument('--format', type=str, help=(
        'ffmpeg mode input image format:',
        'eg: python -m ffhelper im2vid -i images/ -f %05d.jpg'
    ), default=None)
    parser.add_argument('-im', '--img_format', type=str, help='glob mode image format (default is jpg). Ignored when --format is provided.', default='.jpg')
    parser.add_argument('-y', '--override', help='yes if override', action='store_true')
    parser.add_argument('-o', '--output', type=str, help='output file name (default= output.mp4)', default='output.mp4')
    parser.add_argument('-f', '--fps', help='fps rate (-1 to use default)', default=-1)

    return parser.parse_args()


def make_temp_file_list(ls: List[str]) -> str:
    ls = [f"file '{x}'\n" for x in ls]
    filepath = Path(__file__)
    temp_path = filepath.parent / 'video_from_images_temp.txt'
    with open(temp_path, 'w') as f:
        f.writelines(ls)
    return temp_path


def main(additional: bool = False):
    args = parse_args(additional)

    path = args.input
    if args.format is not None:
        path = os.path.join(path, args.format)
        temp_path = None
    else:
        search_glob = os.path.join(path, f'*{args.img_format}')
        ls = glob.glob(os.path.join(path, f'*{args.img_format}'))
        if len(ls) == 0:
            print('Cannot find any image in:')
            print(search_glob)
            print('exit...')
            exit()
        temp_path = make_temp_file_list(ls)

    cmd = 'ffmpeg '

    if temp_path is not None:
        cmd += f' -f concat -safe 0 -i "{temp_path}" '
    else:
        cmd += f' -i "{path}" '

    if args.override:
        cmd += '-y '
    if args.fps != -1:
        cmd += f' -vf fps={args.fps} '

    cmd += f'{args.output}'
    print(f'========= video_from_images run: {cmd}')
    os.system(cmd)
    print(f'========= video_from_images done: {cmd}')
    if temp_path is not None:
        os.remove(temp_path)



if __name__ == '__main__':
    main()

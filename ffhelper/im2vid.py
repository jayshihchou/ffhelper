import argparse
import glob
from io import FileIO
import os
import tempfile
from pathlib import Path
from typing import List


def parse_args(subparser: argparse._SubParsersAction = None) -> argparse.ArgumentParser:
    parser = subparser.add_parser('im2vid') if subparser is not None else argparse.ArgumentParser()

    parser.add_argument('-i', '--input', type=str, help='input image path', required=True)
    parser.add_argument('--format', type=str, help=(
        'ffmpeg mode input image format'
        '\n(eg: ffhelper im2vid -i images/ -f %%05d.jpg)'
    ), default=None)
    parser.add_argument('-im', '--img_format', type=str, help='glob mode image format (default is jpg). Ignored when --format is provided.', default='.jpg')
    parser.add_argument('-y', '--override', help='yes if override', action='store_true')
    parser.add_argument('-o', '--output', type=str, help='output file name (default= output.mp4)', default='output.mp4')
    parser.add_argument('-f', '--fps', help='fps rate (-1 to use default)', default=-1)
    parser.add_argument('-q', '--quality', type=int, help='quality option -crf in ffmpeg, (best 0 ~ 51 worst, -1 to use default 23)', default=-1)

    parser.format_help

    if subparser is None:
        return parser.parse_args()

    parser.set_defaults(func=main)

    return None


def make_temp_file_list(ls: List[str]) -> FileIO:
    ls = [f"file '{x}'\n" for x in ls]

    f = tempfile.NamedTemporaryFile(delete=False)
    f.writelines(ls)
    return f


def main(args: argparse.Namespace = None) -> None:
    if args is None:
        args = parse_args()

    path = args.input
    if args.format is not None:
        path = os.path.join(path, args.format)
        temp_file = None
    else:
        search_glob = os.path.join(path, f'*{args.img_format}')
        ls = glob.glob(os.path.join(path, f'*{args.img_format}'))
        if len(ls) == 0:
            print('Cannot find any image in:')
            print(search_glob)
            print('exit...')
            exit()
        temp_file = make_temp_file_list(ls)

    try:
        cmd = 'ffmpeg '

        if temp_file is not None:
            cmd += f' -f concat -safe 0 -i "{temp_file.name}" '
        else:
            cmd += f' -i "{path}" '

        if args.override:
            cmd += '-y '
        if args.fps != -1:
            cmd += f' -vf fps={args.fps} '

        if args.quality != -1:
            assert args.quality > -1 and args.quality < 52, 'quality only support between [0, 51] (-1 to use default 23)'
            cmd += f' -crf {args.quality} '

        cmd += f'{args.output}'
        print(f'========= video_from_images run: {cmd}')
        os.system(cmd)
        print(f'========= video_from_images done: {cmd}')
    except Exception as e:
        raise e
    finally:
        if temp_file is not None:
            temp_file.close()



if __name__ == '__main__':
    main()

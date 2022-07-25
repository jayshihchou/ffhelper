import argparse
import os

max_input = 16 + 1


def parse_args(subparser: argparse._SubParsersAction = None) -> argparse.ArgumentParser:
    parser = subparser.add_parser('join') if subparser is not None else argparse.ArgumentParser()

    for i in range(1, max_input):
        parser.add_argument(f'-i{i}', f'--input{i}', type=str, help='input video {i}')
    parser.add_argument('-y', '--override', help='yes if override', action='store_true')
    parser.add_argument('-o', '--output', type=str, help='output file name (default= output.mp4)', default='output.mp4')
    parser.add_argument('--no_audio', help='yes if no audio', action='store_true')

    if subparser is None:
        return parser.parse_args()

    parser.set_defaults(func=main)

    return None


def main(args: argparse.Namespace = None):
    if args is None:
        args = parse_args()
    no_audio = args.no_audio
    ls = []
    for i in range(1, max_input):
        if args.__dict__[f'input{i}'] is not None:
            ls.append(args.__dict__[f'input{i}'])
    cmd = 'ffmpeg '
    if args.override:
        cmd += '-y '
    for i in range(len(ls)):
        cmd += f'-i {ls[i]} '
    cmd += '-filter_complex "'

    for i in range(len(ls)):
        cmd += f'[{i}:v] ' if no_audio else f'[{i}:v] [{i}:a] '

    cmd += f'concat=n={len(ls)}:v=1'
    if not no_audio:
        cmd += ':a=1 '
    cmd += '[v]'
    if not no_audio:
        cmd += ' [a]'
    cmd += '" '
    cmd += '-map "[v]" '
    if not no_audio:
        cmd += '-map "[a]" '
    cmd += f'{args.output}'
    print(f'========= append_video run: {cmd}')
    os.system(cmd)
    print(f'========= append_video done: {cmd}\n (If you running into error \"matches no streams\" try add --no_audio.\n  Currently it only works when videos are same resolution)')


if __name__ == '__main__':
    main()

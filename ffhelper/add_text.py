import argparse
import os
from typing import Union

max_input = 16 + 1


def parse_args(subparser: argparse._SubParsersAction = None) -> argparse.ArgumentParser:
    parser = subparser.add_parser('add_text') if subparser is not None else argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, help='input video', required=True)
    parser.add_argument('-y', '--override', help='yes if override', action='store_true')
    parser.add_argument('-o', '--output', type=str, help='output file name (default= output.mp4)', default='output.mp4')
    for i in range(1, max_input):
        parser.add_argument(f'-t{i}', f'--text{i}', type=str, help=f'input text {i}')
        parser.add_argument(f'-p{i}', f'--pos{i}', type=str, help=f'text {i} position format: x=??:y=?? example: x=(main_w-text_w-10):y=(main_h-text_h-10)  (this = right_bottom)', default=None)
        parser.add_argument(f'-s{i}', f'--size{i}', type=str, help=f'text {i} font size (int)', default=None)
        parser.add_argument(f'-c{i}', f'--color{i}', type=str, help=f'text {i} font color (string) example: white', default=None)
        parser.add_argument(f'-f{i}', f'--font{i}', type=str, help=f'text {i} font type (string) example: Arial', default=None)
        parser.add_argument(f'-nb{i}', f'--no_background{i}', help=f'yes if don\'t need to draw background for text {i}', action='store_true')
        parser.add_argument(f'-bc{i}', f'--background_color{i}', type=str, help=f'background color for text {i}', default=None)
        parser.add_argument(f'-ba{i}', f'--background_alpha{i}', type=float, help=f'background alpha for text {i} float value [0.0 ~ 1.0]', default=None)
        parser.add_argument(f'-bb{i}', f'--background_border{i}', type=str, help=f'background border size for text {i}', default=None)

    parser.add_argument('-s', '--size', type=str, help='set all default font size will be replace by -s{number}')
    parser.add_argument('-c', '--color', type=str, help='set all default font color will be replace by -c{number}')
    parser.add_argument('-f', '--font', type=str, help='set all default font will be replace by -f{number}')
    parser.add_argument('-b', '--background', help='set all default draw background', action='store_true')
    parser.add_argument('-bc', '--background_color', type=str, help='set all default background color', default='black')
    parser.add_argument('-ba', '--background_alpha', type=float, help='set all default background alpha float value [0.0 ~ 1.0]', default=1.0)
    parser.add_argument('-bb', '--background_border', type=str, help='set all default background border size', default=5)

    if subparser is None:
        return parser.parse_args()

    parser.set_defaults(func=main)

    return None


def parse_text(args: argparse.ArgumentParser, i: int) -> Union[None, str]:
    if args.__dict__[f'text{i}'] is None:
        return None

    text = args.__dict__[f'text{i}']
    text_cmd = ''
    if i != 1:
        text_cmd += ','
    text_cmd += f'drawtext=text={text}'

    if args.__dict__[f'font{i}'] is not None:
        text_cmd += ':font=' + args.__dict__[f'font{i}']
    elif args.__dict__['font'] is not None:
        text_cmd += ':font=' + args.__dict__['font']

    if args.__dict__[f'pos{i}'] is not None:
        text_cmd += ':' + args.__dict__[f'pos{i}']
    else:
        text_cmd += ':x=0:y=0'

    if args.__dict__[f'size{i}'] is not None:
        text_cmd += ':fontsize=' + args.__dict__[f'size{i}']
    elif args.__dict__['size'] is not None:
        text_cmd += ':fontsize=' + args.__dict__['size']

    if args.__dict__[f'color{i}'] is not None:
        text_cmd += ':fontcolor=' + args.__dict__[f'color{i}']
    elif args.__dict__['color'] is not None:
        text_cmd += ':fontcolor=' + args.__dict__['color']

    if args.__dict__['background']:
        if args.__dict__[f'no_background{i}']:
            return text_cmd
        background_color = args.__dict__['background_color']
        if args.__dict__[f'background_color{i}'] is not None:
            background_color = args.__dict__[f'background_color{i}']
        text_cmd += f':box=1:boxcolor={background_color}'

        background_alpha = args.__dict__['background_alpha']
        if args.__dict__[f'background_alpha{i}'] is not None:
            background_alpha = args.__dict__[f'background_alpha{i}']
        if background_alpha != 1.0:
            text_cmd += f'@{background_alpha}'

        background_border = args.__dict__['background_border']
        if args.__dict__[f'background_border{i}'] is not None:
            background_border = args.__dict__[f'background_border{i}']
        text_cmd += f':boxborderw={background_border}'

    return text_cmd


def main(args: argparse.Namespace = None):
    if args is None:
        args = parse_args()

    path = args.input

    cmd = f'ffmpeg -i "{path}" '

    if args.override:
        cmd += '-y '

    cmd += '-vf '

    for i in range(1, max_input):
        text_cmd = parse_text(args, i)
        if text_cmd is not None:
            cmd += text_cmd

    cmd += f' {args.output}'
    print(f'========= add_text run: {cmd}')
    os.system(cmd)
    print(f'========= add_text done: {cmd}')



if __name__ == '__main__':
    main()

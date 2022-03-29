import argparse
import os
from typing import Dict, List, Tuple

name_tag = '0123456789abcdefghijklmnopqrstuvwxyz'
max_input = 16 + 1


def parse_args(additional: bool = False) -> argparse.ArgumentParser:
    global max_input
    parser = argparse.ArgumentParser()
    if additional:
        parser.add_argument('COMMAND', help='command to use')
    for i in range(1, max_input):
        parser.add_argument(f'-i{i}', f'--input{i}', type=str, help='input video {i}')
        parser.add_argument(f'-c{i}', f'--crop{i}', type=str, help='crop {i} usage: -c{i} w:h:x:y', default=None)
        parser.add_argument(f'-s{i}', f'--scale{i}', type=str, help='scale {i} usage: -s{i} w:h', default=None)
    parser.add_argument('-m', '--map', type=str, help='mapping')
    parser.add_argument('-v', '--vertical', help='vertical mode', action='store_true')
    parser.add_argument('-y', '--override', help='yes if override', action='store_true')
    parser.add_argument('-o', '--output', type=str, help='output file name (default = output.mp4)', default='output.mp4')
    return parser.parse_args()


def parse_map_index(s: str) -> Dict:
    res = []
    if '+' in s:
        plus_ls = s.split('+')
        for e in plus_ls:
            res.append(parse_map_index(e))
        return res
    if '*' in s:
        mul_ls = s.split('*')
        if len(mul_ls) != 2:
            raise ValueError(f'parse mapping error: {s}')
        res = {'v': int(mul_ls[0]) - 1, 'alpha': float(mul_ls[1])}
    else:
        res = {'v': int(s) - 1}
    return res


def parse_map(mapping: str) -> List[str]:
    res = []
    for each in mapping.split(','):
        res.append(parse_map_index(each))

    return res


def video_to_str(m: dict, args: argparse.ArgumentParser, tag_name: str, width: int = None, vertical: bool = False) -> str:
    v = m['v']
    mcmd = f'[{v}:v]setpts=PTS-STARTPTS'
    v += 1
    if args.__dict__[f'crop{v}'] is not None:
        mcmd += ', crop=' + args.__dict__[f'crop{v}']
    if args.__dict__[f'scale{v}'] is not None:
        mcmd += ', scale=' + args.__dict__[f'scale{v}']
    if 'alpha' in m:
        alpha = m['alpha']
        mcmd += f', format=yuva420p,colorchannelmixer=aa={alpha}'
    if width is not None:
        if vertical:
            mcmd += f', pad=iw:ih*{width}'
        else:
            mcmd += f', pad=iw*{width}:ih'

    mcmd += f'[{tag_name}];'

    return mcmd


def map_to_str(map_ls: List[dict], args: argparse.ArgumentParser, index: int) -> Tuple[str, str, int]:
    global name_tag
    mcmd = ''
    last_tag = ''
    for j in range(len(map_ls) - 1):
        last_tag = name_tag[j]
        mcmd += video_to_str(map_ls[j], args, last_tag)
        if j + 1 != len(map_ls):
            tag1 = last_tag
            last_tag = name_tag[j + 1]
            mcmd += video_to_str(map_ls[j + 1], args, last_tag)
            tag2 = last_tag

            last_tag = name_tag[index]
            index += 1
            mcmd += f'[{tag1}][{tag2}] overlay=shortest=1[{last_tag}];'

    return mcmd, last_tag, index


def main(additional: bool = False):
    global name_tag, max_input
    args = parse_args(additional)
    ls = []
    for i in range(1, max_input):
        if args.__dict__[f'input{i}'] is not None:
            ls.append(args.__dict__[f'input{i}'])

    mapping = args.map

    if mapping is None:
        mapping = ''
        for i in range(len(ls)):
            f = ls[i]
            if f is not None:
                if i == 0:
                    mapping += f'{i}'
                else:
                    mapping += f', {i}'

    mapping = parse_map(mapping)

    width = len(mapping)
    cmd = 'ffmpeg '
    if args.override:
        cmd += '-y '
    for i in range(len(ls)):
        cmd += f'-i {ls[i]} '
    cmd += '-q:v 2 '
    cmd += '-filter_complex "'

    index = width + 1

    tags = {}
    for i in range(len(mapping)):
        m_ls = mapping[i]
        if len(m_ls) > 1:
            mcmd, tag, index = map_to_str(m_ls, args, index)
            cmd += mcmd
            tags[i] = tag

    cmd += ''
    for i in range(len(mapping)):
        if i not in tags:
            m_ls = mapping[i]
            cmd += video_to_str(m_ls, args, name_tag[i], width if i == 0 else None, args.vertical)
            tags[i] = name_tag[i]

    last_tag = tags[0]

    if args.vertical:
        for i in range(len(mapping) - 1):
            tag1 = last_tag
            tag2 = tags[i + 1]

            last_tag = name_tag[index]
            index += 1
            cmd += f'[{tag1}][{tag2}]overlay=0:H*{i + 1}/{width}[{last_tag}];'
    else:
        for i in range(len(mapping) - 1):
            tag1 = last_tag
            tag2 = tags[i + 1]

            last_tag = name_tag[index]
            index += 1
            cmd += f'[{tag1}][{tag2}]overlay=W*{i + 1}/{width}:0[{last_tag}];'

    cmd = cmd[:-1]
    cmd += '"'

    cmd += f' -map "[{last_tag}]" {args.output}'
    print(f'========= cat_video run: {cmd}')
    os.system(cmd)
    print(f'========= cat_video done: {cmd}')


if __name__ == '__main__':
    main()

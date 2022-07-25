import argparse
import sys

from ffhelper.__version__ import __version__
from ffhelper import _parse_args_add_text, _parse_args_combine, _parse_args_dump, _parse_args_im2vid, _parse_args_join


def main():
    parse_func_list = [
        _parse_args_add_text,
        _parse_args_combine,
        _parse_args_dump,
        _parse_args_im2vid,
        _parse_args_join,
    ]
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-v', '--version', action='store_true', help='print_version')
    subparser = parser.add_subparsers(help=(
        'commands:'
        '\n    combine           combine videos'
        '\n    join              join videos'
        '\n    dump              dump images/audio/metadata or replace audio'
        '\n    im2vid            make video from image folder'
        '\n    add_text          adding label into video'
    ))

    for f in parse_func_list:
        f(subparser)

    args = parser.parse_args()
    
    if 'func' in args:
        args.func(args)
    elif args.version:
        print('ffhelper', __version__)
    else:
        parser.print_usage()


if __name__ == '__main__':
    main()

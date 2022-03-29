import sys

from ffhelper import __version__, add_text, combine, dump, im2vid, join


def print_help():
    print(
        'Usage: python -m ffhelper [COMMAND] [OPTIONS]'
        '\n\nCommands:'
        '\n    combine           combine videos'
        '\n    join              join videos'
        '\n    dump              dump images/audio/metadata or replace audio'
        '\n    im2vid            make video from image folder'
        '\n    add_text          adding label into video'
        '\n    -v, --version     show version'
        '\n adding command to see more help info'
    )


def main():
    cmds = {
        'combine': combine,
        'join': join,
        'dump': dump,
        'im2vid': im2vid,
        'add_text': add_text,
    }
    if len(sys.argv) == 1:
        print('Need to provide method to use.')
        print_help()
        exit()
    if sys.argv[1] == '-h' or sys.argv[1] == '--help':
        print_help()
        exit()
    if sys.argv[1] == '-v' or sys.argv[1] == '--version':
        print('ffhelper', __version__)
        exit()
    all_not_in_cmd = True
    cmd = None
    for i in range(1, len(sys.argv)):
        cmd = sys.argv[i]
        if cmd in cmds:
            all_not_in_cmd = False
            break
    if all_not_in_cmd:
        print('No method named:', sys.argv[1])
        print_help()
        exit()

    cmds[sys.argv[1]].main(True)


if __name__ == '__main__':
    main()

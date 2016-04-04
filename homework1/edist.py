#! /usr/bin/env python
# Need Python3 Runtime
import sys
from optparse import OptionParser


INSERT_COST = 1
DELETE_COST = 1
SUBSTITUTION_COST = 2


def file_mode(file):
    argv_generator = from_file(file)
    for argv in argv_generator:
        do_min_edit_distance(argv[0], argv[1])


def from_file(file):
    while True:
        try:
            raw_argv = file.readline()
        except Exception:
            return
        # EOF
        if not raw_argv:
            return
        raw_argv = raw_argv.strip()
        if not raw_argv:
            continue
        argv = raw_argv.split(' ')
        if len(argv) != 2:
            parser.error(args_err)

        yield argv


def min_edit_distance(dst, src):
    dm = [[0 for i in range(len(src) + 1)] for j in range(len(dst) + 1)]
    for i in range(1, len(src) + 1):
        dm[0][i] = i
    for i in range(1, len(dst) + 1):
        dm[i][0] = i
    for i in range(1, len(dst) + 1):
        for j in range(1, len(src) + 1):
            dm[i][j] = min(dm[i - 1][j] + ins_cost(dst[i - 1]),
                           dm[i - 1][j - 1] + sub_cost(dst[i - 1], src[j - 1]),
                           dm[i][j - 1] + del_cost(src[j - 1]))
    return dm[len(dst)][len(src)]


def do_min_edit_distance(dst, src):
    dist = min_edit_distance(dst, src)
    if opts.output_mode:
        print('%s => %s: %d' % (src, dst, dist))
    else:
        print(dist)


def ins_cost(rune):
    return INSERT_COST


def del_cost(rune):
    return DELETE_COST


def sub_cost(dst, src):
    if dst == src:
        return 0
    else:
        return SUBSTITUTION_COST


def main():
    if opts.input_mode:
        file_mode(sys.stdin)
    elif opts.filename:
        file_mode(open(opts.filename))
    else:
        do_min_edit_distance(args[0], args[1])


if __name__ == '__main__':
    usage = 'Usage: %prog [-s|-l] [-c|-f FILENAME] [dst_str src_str]'
    args_err = 'need two extra args as input strings'
    parser = OptionParser(usage=usage)
    parser.add_option('-c', '--stdin', action='store_true', dest='input_mode', default=False,
                      help='input with stdin, without extra args')
    parser.add_option('-s', '--short', action='store_false', dest='output_mode', default=False,
                      help='result print in short mode')
    parser.add_option('-l', '--long', action='store_true', dest='output_mode', help='result print in long mode')
    parser.add_option('-f', '--file', dest='filename', help='input with a file')
    opts, args = parser.parse_args()
    if len(args) == 0 and (not opts.filename):
        opts.input_mode = True
    if (not opts.input_mode) and len(args) != 2 and (not opts.filename):
        parser.error(args_err)
    if opts.input_mode and len(args) > 0:
        parser.error('too many args with stdin mode')
    main()

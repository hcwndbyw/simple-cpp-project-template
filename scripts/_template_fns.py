from __future__ import print_function

import sys
import os
import argparse


def get_path_of_target_under(target, under):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    root_dir = os.path.dirname(script_dir)
    return os.path.join(os.path.join(root_dir, under), target)


def component_exists(lib):
    path = get_path_of_target_under(lib, "src")
    return os.path.exists(path)


def print_error(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def create_file_in_target_under(target, under, lines, filename):
    path = get_path_of_target_under(target, under)
    if not os.path.exists(path):
        os.mkdir(path)

    filewithpath = os.path.join(path, filename)
    if os.path.exists(filewithpath):
        print_error("Internal error! {} already exists!".format(filewithpath))
        sys.exit(1)

    with open(filewithpath, "a+") as f:
        f.write('\n'.join(lines))


def create_cmakelists_for_target_under(target, under, lines):
    create_file_in_target_under(target, under, lines, 'CMakeLists.txt')


def add_dir_to_root_cmakelists(name, under):
    path = get_path_of_target_under('CMakeLists.txt', under)
    if not os.path.exists(path):
        print_error("Internal error! This should not be! Attempt to append to a non-existing root CMakeLists.txt")
        sys.exit(1)

    with open(path, "a+") as f:
        f.write("add_subdirectory({})\n".format(name))


def build_target_link_lines(target_name, to_link):
    def indent(s):
        return '    {}'.format(s)

    target_link_libs_template = "target_link_libraries( {}"
    lines = []

    if len(to_link) > 0:
        lines.append("")
        lines.append(target_link_libs_template.format(target_name))
        lines.extend(map(indent, to_link))
        lines.append(")")

    return lines


def parse_args(is_lib):
    desc = "Generates a new {} under src"
    if is_lib:
        desc = desc.format('lib')
    else:
        desc = desc.format('executable')

    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('name', metavar='name', type=str, nargs=1,
                        help='Name of lib or bin to create')

    parser.add_argument('-no-glob', dest='no_glob',
                        action='store_const', const=True, default=False,
                        help='If set, sources for this target will not use globs. \
                        You will have to explicitly list source files.')

    parser.add_argument('-link', dest='to_link', type=str, nargs='+', default=[],
                        help='An optional list of libraries to link to.')

    args = parser.parse_args()

    args.name = args.name[0].lower()

    if component_exists(args.name):
        typ = "binary"
        if is_lib:
            typ = 'lib'
        print_error("{} {} already exists!".format(typ, args.name))
        sys.exit(1)

    return args

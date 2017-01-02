from __future__ import print_function

import sys
import os


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
        f.write("add_subdirectory({})".format(name))

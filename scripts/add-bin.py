#!/usr/bin/python
import _template_fns as tf


def build_lines_for_bin(bin_name, link):
    glob_template = "file( GLOB {} ./*.cpp ./*.c ./*.cxx )"
    add_bin_template = "add_executable( {} ${{{}}} )"
    target_link_libs_template = "target_link_libraries( {}"

    glob_name = '{}_SRC'.format(bin_name.upper())

    lines = [
        glob_template.format(glob_name),
        add_bin_template.format(bin_name, glob_name),
    ]

    if len(link) > 0:
        lines.append("")
        lines.append(target_link_libs_template.format(bin_name))
        # TODO indent
        lines.extend(link)
        lines.append(")")

    return lines


def main():
    args = tf.parse_args(False)
    bin_name = args.name

    lines = build_lines_for_bin(bin_name, [])
    tf.create_cmakelists_for_target_under(bin_name, "src", lines)
    cpp_lines = ['int main() { return 0; }']
    tf.create_file_in_target_under(bin_name, "src", cpp_lines, "{}.cpp".format(bin_name))

    tf.add_dir_to_root_cmakelists(bin_name, "src")

if __name__ == '__main__':
    main()

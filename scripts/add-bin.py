#!/usr/bin/python
import _template_fns as tf


def build_lines_for_bin(bin_name, link, no_glob, to_link):
    srcs_template = "file( GLOB {} ./*.cpp ./*.c ./*.cxx )"
    add_bin_template = "add_executable( {} ${{{}}} )"

    srcs_name = '{}_SRC'.format(bin_name.upper())

    if no_glob:
        srcs_template = "set( {{}}\n    {}.cpp\n    # Add new source files here\n)".format(bin_name)

    lines = [
        srcs_template.format(srcs_name),
        "",
        add_bin_template.format(bin_name, srcs_name),
    ]

    lines.extend(tf.build_target_link_lines(bin_name, to_link))

    return lines


def main():
    args = tf.parse_args(False)
    bin_name = args.name

    lines = build_lines_for_bin(bin_name, [], args.no_glob, args.to_link)
    tf.create_cmakelists_for_target_under(bin_name, "src", lines)
    cpp_lines = ['int main() { return 0; }']
    tf.create_file_in_target_under(bin_name, "src", cpp_lines, "{}.cpp".format(bin_name))

    tf.add_dir_to_root_cmakelists(bin_name, "src")

if __name__ == '__main__':
    main()

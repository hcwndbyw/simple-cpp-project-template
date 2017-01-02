#!/usr/bin/python
import _template_fns as tf


def build_lines_for_test_cmake(lib_name, no_glob):
    files = "file(GLOB {}_TEST_SOURCES ./*.cpp ./*.c ./*.cxx )".format(lib_name.upper())
    if no_glob:
        files = "set( {}_TEST_SOURCES\n    {}_test.cpp\n    # Add new source files here\n)".format(lib_name.upper(),
                                                                                                   lib_name)
    lines = [
        "include_directories( ${CMAKE_SOURCE_DIR}/src )",
        "include_directories( ${GTEST_INCLUDES} )",
        files,
        "",
        "add_executable( {}_test".format(lib_name),
        "    ${{{}_TEST_SOURCES}}".format(lib_name.upper()),
        ")",
        "",
        "target_link_libraries( {}_test".format(lib_name),
        "    {}".format(lib_name),
        "    GTestMain",
        ")",
        "",
        "set_target_properties( {}_test".format(lib_name),
        "    PROPERTIES",
        "    ARCHIVE_OUTPUT_DIRECTORY ${TEST_ARCHIVE_OUTPUT_DIRECTORY}",
        "    LIBRARY_OUTPUT_DIRECTORY ${TEST_LIBRARY_OUTPUT_DIRECTORY}",
        "    RUNTIME_OUTPUT_DIRECTORY ${TEST_RUNTIME_OUTPUT_DIRECTORY}",
        ")",
        "",
        "add_custom_command(",
        "    TARGET {}_test".format(lib_name),
        "    COMMAND ${{TEST_RUNTIME_OUTPUT_DIRECTORY}}/{}_test".format(lib_name),
        "    POST_BUILD",
        ")",
        "",
        "add_test ({}_test_run".format(lib_name),
        "    ${{TEST_RUNTIME_OUTPUT_DIRECTORY}}/{}_test".format(lib_name),
        ")",
    ]
    return lines


def build_lines_for_lib(lib_name, no_glob, to_link, lib_type):
    srcs_template = "file( GLOB {} ./*.cpp ./*.c ./*.cxx )"
    add_lib_template = "add_library( {}{} ${{{}}} )"

    srcs_name = '{}_SRC'.format(lib_name.upper())

    if no_glob:
        srcs_template = "set( {{}}\n    {}.cpp\n    # Add new source files here\n)".format(lib_name)

    lines = [
        srcs_template.format(srcs_name),
        "",
        add_lib_template.format(lib_name, lib_type, srcs_name),
        "",
        "add_subdirectory( tests )"
    ]

    lines.extend(tf.build_target_link_lines(lib_name, to_link))

    return lines


def build_lines_for_test(lib_name):
    lines = [
        '#include "gtest/gtest.h"',
        "",
        "class {}_test : public ::testing::Test {{}};".format(lib_name),
        "TEST_F({}_test, Fails)".format(lib_name),
        "{ EXPECT_EQ(true, false); }"
    ]
    return lines


def main():
    args = tf.parse_args(True)
    lib_name = args.name

    lines = build_lines_for_lib(lib_name, args.no_glob, args.to_link, args.lib_type)
    tf.create_cmakelists_for_target_under(lib_name, "src", lines)
    tf.create_file_in_target_under(lib_name, "src", ["#pragma once"], "{}.h".format(lib_name))
    cpp_lines = ['#include "{}.h"'.format(lib_name)]
    tf.create_file_in_target_under(lib_name, "src", cpp_lines, "{}.cpp".format(lib_name))

    test_lines = build_lines_for_test_cmake(lib_name, args.no_glob)
    tf.create_cmakelists_for_target_under("tests", "src/{}".format(lib_name), test_lines)

    unit_test_lines = build_lines_for_test(lib_name)
    tf.create_file_in_target_under("tests", "src/{}".format(lib_name), unit_test_lines, "{}_test.cpp".format(lib_name))

    tf.add_dir_to_root_cmakelists(lib_name, "src")


if __name__ == '__main__':
    main()

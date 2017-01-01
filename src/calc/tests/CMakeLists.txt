include_directories( ${CMAKE_SOURCE_DIR}/src )
include_directories( ${GTEST_INCLUDES} )

set( calc_test_sources
    CalcTest.cpp
)

add_executable( calc_test
    ${calc_test_sources}
)

target_link_libraries( calc_test
    calc
    GTestMain
)

set_target_properties( calc_test
    PROPERTIES
    ARCHIVE_OUTPUT_DIRECTORY ${TEST_ARCHIVE_OUTPUT_DIRECTORY}
    LIBRARY_OUTPUT_DIRECTORY ${TEST_LIBRARY_OUTPUT_DIRECTORY}
    RUNTIME_OUTPUT_DIRECTORY ${TEST_RUNTIME_OUTPUT_DIRECTORY}
)

add_custom_command(
    TARGET calc_test
    COMMAND ${TEST_RUNTIME_OUTPUT_DIRECTORY}/calc_test
    POST_BUILD
)

add_test (calc_test_run
    ${TEST_RUNTIME_OUTPUT_DIRECTORY}/calc_test
)

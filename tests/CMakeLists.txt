message( STATUS ${CMAKE_SOURCE_DIR} )

include_directories( ${CMAKE_SOURCE_DIR}/src )
include_directories( ${GTEST_INCLUDES} )

set( test_sources
    CalcTest.cpp )

add_executable( AllTests
    ${test_sources})

target_link_libraries( AllTests
    calc
    GTestMain
)

add_custom_command(
    TARGET AllTests
    POST_BUILD
    COMMAND AllTests
)

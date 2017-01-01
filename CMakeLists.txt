cmake_minimum_required( VERSION 2.6 )
message("${CMAKE_SOURCE_DIR}")
message("${CMAKE_BINARY_DIR}")
if("${CMAKE_SOURCE_DIR}" STREQUAL "${CMAKE_BINARY_DIR}")
    message(FATAL_ERROR "In-source builds are not  are not permitted. Make a separate folder for building:\n\tmkdir build; cd build; cmake ..\nBefore that, remove the files already created:\n\trm -rf CMakeCache.txt CMakeFiles")
endif("${CMAKE_SOURCE_DIR}" STREQUAL "${CMAKE_BINARY_DIR}")

project( ProjectName )

add_definitions( -std=c++14 )

# Set BOOST_ROOT environment variable to point to your local Boost dir.
find_package( Boost REQUIRED )
include_directories( ${Boost_INCLUDE_DIR} )

# Get gtest dependency
find_package(Threads REQUIRED)
include(ExternalProject)

set(GTEST_PREFIX "${CMAKE_CURRENT_BINARY_DIR}/gtest")
ExternalProject_Add(GTestExternal
    GIT_REPOSITORY https://github.com/google/googletest
    GIT_TAG master
    TIMEOUT 10
    PREFIX "${GTEST_PREFIX}"
    INSTALL_COMMAND "")

set(LIBPREFIX "${CMAKE_STATIC_LIBRARY_PREFIX}")
set(LIBSUFFIX "${CMAKE_STATIC_LIBRARY_SUFFIX}")
set(GTEST_LOCATION "${GTEST_PREFIX}/src/GTestExternal-build")
set(GTEST_INCLUDES "${GTEST_PREFIX}/src/GTestExternal/googletest/include")
set(GTEST_LIBRARY  "${GTEST_LOCATION}/googlemock/gtest/${LIBPREFIX}gtest${LIBSUFFIX}")
set(GTEST_MAINLIB  "${GTEST_LOCATION}/googlemock/gtest/${LIBPREFIX}gtest_main${LIBSUFFIX}")

add_library(GTest IMPORTED STATIC GLOBAL)
set_target_properties(GTest PROPERTIES
    IMPORTED_LOCATION                 "${GTEST_LIBRARY}"
    INTERFACE_INCLUDE_DIRECTORIES     "${GTEST_INCLUDES}"
    IMPORTED_LINK_INTERFACE_LIBRARIES "${CMAKE_THREAD_LIBS_INIT}")

add_library(GTestMain IMPORTED STATIC GLOBAL)
set_target_properties(GTestMain PROPERTIES
    IMPORTED_LOCATION "${GTEST_MAINLIB}"
    IMPORTED_LINK_INTERFACE_LIBRARIES
        "${GTEST_LIBRARY};${CMAKE_THREAD_LIBS_INIT}")

add_dependencies(GTest GTestExternal)

IF (NOT CMAKE_BUILD_TYPE )
    SET ( CMAKE_BUILD_TYPE Debug )
ENDIF()

string(TOUPPER "${CMAKE_BUILD_TYPE}" uppercase_CMAKE_BUILD_TYPE)

message("CMAKE_BUILD_TYPE = ${CMAKE_BUILD_TYPE}")
IF(NOT uppercase_CMAKE_BUILD_TYPE MATCHES "^(DEBUG|RELEASE)$")
    message(FATAL_ERROR "Unrecognized build flavor. Only Debug and Release are supported.")
ENDIF()

set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

set(TEST_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/tests/lib)
set(TEST_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/tests/lib)
set(TEST_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/tests/bin)

enable_testing()

add_subdirectory( src )

add_custom_target(loop
    COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/scripts/LoopBuild.sh)

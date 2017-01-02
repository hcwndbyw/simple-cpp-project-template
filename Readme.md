# New CPP project template

A simple c++ project template with a focus on getting up and running quickly and good separation of components. If you have a small or simple project, you may never need to touch any build logic. This template relies on cmake, googletest and python.

## Quick start
    ./scripts/add-lib.py my_library
    ./scripts/add-bin.py my_executable -l my_library
    make [debug|release]


This sequence of commands will create a library called `my_library`, add a failing unit test for `my_library`, add a new binary `my_executable` that takes a link dependency on `my_library`, build everything, then run unit tests.

## Project Structure

After running the above, your project Structure should look something like the following:

```
project/
| debug/
| scripts/
| src/
| | my_executable/
| | | my_executable.cpp
| | | CMakeLists.txt
| | my_library/
| | | tests/
| | | | my_library_test.cpp
| | | | CMakeLists.txt
| | | my_library.h
| | | my_library.cpp
| | | CMakeLists.txt
| | CMakeLists.txt
| CMakeLists.txt
| Makefile
```

Components end up in their own directories under src, and make targets are generated per component. Libraries each get a `tests` subdirectory. Keeping things separate is nice - at least I think so. By convention all components use lower-case names - the `add-bin` and `add-lib` scripts enforce this.

To remove an added component, just delete the directory and remove the corresponding line in `src/CMakeLists.txt`

## Tools
### scripts
Two included python scripts `add-lib` and `add-bin` take care of setting up the build-goo for new libraries and binaries. Each require a single command line argument for the name of the new component. See the help output for more information (`add-lib -h`). By default, both of these scripts use `GLOB` patterns for `*.c`, `*.cpp`, and `*.cxx` for enumerating sources files. This means you don't have to manually list your source files in the respective `CMakeLists.txt` file - which can be a problem in some situations. The `-no-glob` argument allows you to use explicit source file lists instead.

### Top level makefile
There's a top-level makefile that provides some convince targets to take care of creating build directors, calling cmake, etc.

## Building
In-source builds are not allowed - builds must take place in a new directory (usually debug or release). While the top-level Makefile provides some shortcuts, you can get at all the provided target by running `make` in the build directory.

```
mkdir build
cd build
cmake ..
make
make my_library
```

## Build output
```
project/
| debug/
| | CMakeFiles/
| | bin/
| | | my_executable*
| | gtest/
| | lib/
| | | libmy_library.a
| | src/
| | tests/
| | | bin/
| | CMakeCache.txt
| | CTestTestfile.cmake
| | Makefile
| | cmake_install.cmake
| | compile_commands.json
| scripts/
| src/
| CMakeLists.txt
| Makefile
```

Generated files land in the build directory with executables under `bin`, libraries under `lib` and tests under `tests/[lib|bin]`.

New CPP project template
========================

A simple c++ project template using cmake and googletest.  

Usage
--------
    cd build
    cmake ..
    make

`cmake ..` will download googletest for this project automatically.

In addition to building, the `make` command runs all the tests in verbose mode.

`make test` just runs the tests and presents a global summary of tests.

`make loop` uses inotify to watch the src and test directories for changes. When a change is detected, `make` is run again.


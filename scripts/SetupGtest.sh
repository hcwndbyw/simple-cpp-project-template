#! /bin/bash

GTEST="gtest-1.7.0"

pushd "$(git rev-parse --show-toplevel)"
if [ ! -d  "$GTEST" ]; then
    echo "Downloading $GTEST"
    wget http://googletest.googlecode.com/files/"$GTEST".zip
    unzip "$GTEST".zip
    rm "$GTEST".zip
fi
popd

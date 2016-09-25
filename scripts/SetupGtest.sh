#! /bin/bash

GTEST="gtest-1.8.0"

pushd "$(git rev-parse --show-toplevel)"
if [ ! -d  "$GTEST" ]; then
    echo "Downloading $GTEST"
    wget https://github.com/google/googletest/archive/release-1.8.0.zip -O "$GTEST".zip
    unzip "$GTEST".zip
    rm "$GTEST".zip
fi
popd

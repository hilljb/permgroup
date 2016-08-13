#!/bin/bash

WORK_DIR="$(pwd)"

rm -f *.c
rm -f *.pyc
rm -f *.so

if [[ -d "$WORK_DIR/build" ]]; then
    rm -rf build
    echo "- removed build directory"
fi

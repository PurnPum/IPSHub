#!/bin/bash

PATCH_NAME=$1
PATCH_DIR=$2

cd $PATCH_DIR

make

# Check if the expected file was generated
if [ ! -f "$PATCH_NAME" ]; then
    echo "Build failed: $PATCH_NAME not found!"
    exit 1
fi



#!/bin/bash

# Arguments
OUTPUT_PATCH=$1
PATCH_NAME=$2
PATCH_DIR=$3

cd $PATCH_DIR

# Run xdelta to generate a patch file
xdelta3 -e -s ORIGINAL_$PATCH_NAME $PATCH_NAME $OUTPUT_PATCH

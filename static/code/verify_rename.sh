#!/bin/bash

PATCH_NAME=$1
PATCH_DIR=$2
PATCH_SHA=$3

cd $PATCH_DIR

# Get the sha1 of the patch file
PATCH_SHA_GEN=`sha1sum "$PATCH_NAME" | awk '{print $1}'`

# If the sha1 of the patch file is different from the argument PATCH_SHA, there is a problem
if [ "$PATCH_SHA" != "$PATCH_SHA_GEN" ]; then
    echo "Build failed: sha1 ($PATCH_SHA) of $PATCH_NAME does not match PATCH_SHA argument ($PATCH_SHA_GEN)!"
    exit 1
fi

# Rename the original file
mv $PATCH_NAME ORIGINAL_$PATCH_NAME
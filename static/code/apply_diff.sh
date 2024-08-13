#!/bin/bash

IFS=',' read -r -a original_files <<< "$1"
IFS=',' read -r -a filenames <<< "$2"
PATCH_DIR=$3

apply_patch_to_file() {
    patch_file=$1
    target_file=$2

    # Apply the patch to the text file
    # Use the 'diff' command to apply the patch

    patch $target_file < $patch_file
}
# Apply Diffs
cd $PATCH_DIR

for i in "${!original_files[@]}"; do
    patch_file="${filenames[$i]}"
    target_file="${original_files[$i]}"
    echo "Applying $patch_file to $target_file"

    # Call the function with the current pair of values
    apply_patch_to_file "$patch_file" "$target_file"
done
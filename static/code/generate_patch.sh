#!/bin/bash

# Arguments
REPO_URL=$1
REPO_DIR=$2
OUTPUT_PATCH=$3
PATCH_NAME=$4
PATCH_SHA=$5
IFS=',' read -r -a original_files <<< "$6"
IFS=',' read -r -a filenames <<< "$7"

apply_patch_to_file() {
    patch_file=$1
    target_file=$2

    # Apply the patch to the text file
    # Use the 'diff' command to apply the patch
    patch $target_file < $patch_file
}

for file in "${original_files[@]}"; do
    echo "Original file: $file"
done

for filename in "${filenames[@]}"; do
    echo "Filename: $filename"
done

# Clone the repository
git clone $REPO_URL $REPO_DIR
cd $REPO_DIR

# Run the install procedure
make

# Check if the expected file was generated
if [ ! -f "$PATCH_NAME" ]; then
    echo "Build failed: $PATCH_NAME not found!"
    exit 1
fi

# Get the sha1 of the patch file
PATCH_SHA_GEN=`sha1sum "$PATCH_NAME" | awk '{print $1}'`

# If the sha1 of the patch file is different from the argument PATCH_SHA, there is a problem
if [ "$PATCH_SHA" != "$PATCH_SHA_GEN" ]; then
    echo "Build failed: sha1 ($PATCH_SHA) of $PATCH_NAME does not match PATCH_SHA argument ($PATCH_SHA_GEN)!"
    exit 1
fi

# Rename the original file
mv $PATCH_NAME ORIGINAL_$PATCH_NAME

# Apply Diffs

for i in "${!original_files[@]}"; do
    patch_file="${filenames[$i]}"
    target_file="${original_files[$i]}"
    echo "Applying $patch_file to $target_file"

    # Call the function with the current pair of values
    apply_patch_to_file "$patch_file" "$target_file"
done


# Rebuild after replacing files
make clean
make

# Check if the new file was generated
if [ ! -f $PATCH_NAME ]; then
    echo "Build failed: $PATCH_NAME not found!"
    exit 1
fi

# Run xdelta to generate a patch file
xdelta3 -e -s $PATCH_NAME ORIGINAL_$PATCH_NAME > $OUTPUT_PATCH

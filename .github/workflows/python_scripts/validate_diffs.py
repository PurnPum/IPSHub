import os
import shutil
import sys
import argparse
import subprocess
from generate_diffs import clone_game_repo, compile_cloned_game
from pathlib import Path

TEMP_DIR = Path('/tmp/temp_clone')
SUPPORTED_REPOSITORIES = {'pokeyellow': "https://github.com/pret/pokeyellow.git", 'pokecrystal': "https://github.com/pret/pokecrystal.git"}

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="""Takes the structure generated by the generate_diffs.py script and tries to apply the changes to the original code of the game. If it manages to do so
        and the game compilation works, it will finish successfully. Otherwise, it will fail."""
    )
    
    parser.add_argument('-r', '--repository_name', required=True, help='Name of the repository of the original game, use --help to see the list of supported games')
    parser.add_argument('-p', '--patch_dir', default=os.path.join(os.getcwd(),'diffs'), help="Path to the root directory that contains the patch structure (default:" + os.path.join(os.getcwd(),'diffs') + ")")
    parser.add_argument('-k', '--keep_dir', action='store_true', help='Keep the directory with the compiled modified game (default: do not keep)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Make the script output more verbose (default: not verbose)')
    
    args = parser.parse_args()
        
    if args.patch_dir:
        if not os.path.isabs(args.patch_dir):
            args.patch_dir = os.path.join(os.getcwd(), args.patch_dir)

    return args.repository_name, args.patch_dir, args.keep_dir, args.verbose

def build_modified_structure(repo_name, patch_dir, keep_dir, verbose):
    cloned_dir = Path(clone_game_repo(repo_name, verbose))
    for dirpath, _, filenames in os.walk(patch_dir):
        print("Scanning directory:", dirpath)
        if verbose:
            print("Files found:", filenames)
        for filename in filenames:
            if verbose:
                print("Working with file:", filename)
                
            patch_path = Path(dirpath) / filename
            relative_path = patch_path.relative_to(patch_dir)
            temp_target_file = cloned_dir / relative_path
            #Remove the suffix from the file to restore the original one.
            target_file = temp_target_file.with_suffix('')
            
            if verbose:
                print("Patch file:", patch_path)
                print("Relative path:", relative_path)
                print("Target file:", target_file)
            
            if filename.split('.')[-1] == 'patch':
                if verbose:
                    print("Working with patch file:", patch_path)
                apply_patch(patch_path, target_file)
                
            elif filename.split('.')[-1] == 'delete':
                if verbose:
                    print("Working with delete pointer:", patch_path)
                print("Proceeding to delete the file:", target_file)
                delete_pointed_files(target_file)
            else:
                if verbose:
                    print("Found extra file:", patch_path)
                copy_extra_files(patch_path, os.path.dirname(target_file))

    print("Patching process completed, proceeding to attempt to compile the game")
    compile_cloned_game(cloned_dir)

    if not keep_dir and cloned_dir.as_posix().startswith('/tmp/temp_clone/'):
        print("Process finished, cleaning up temporary files located in", cloned_dir)
        shutil.rmtree(cloned_dir)
        
def apply_patch(patch_file, patch_target):
    try:
        with open(patch_file, 'r') as patch_input:
            subprocess.run(['patch', patch_target], stdin=patch_input, check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while patching the file {patch_target} with the patch {patch_file}")
        print("Output:", e.stderr)
        print("Return Code:", e.returncode)
        clean_before_fatal_exit()
    print(f"Successfully patched the file {patch_target} with the patch {patch_file}")
    
def copy_extra_files(file_path, destination_dir):
    try:
        os.makedirs(destination_dir, exist_ok=True)
        shutil.copy2(file_path, destination_dir)
    except OSError as e:
        print(f"An error occurred while copying the file {file_path} to {destination_dir}")
        print("Error code:", e.errno)
        clean_before_fatal_exit()
    print(f"Successfully copied the file {file_path} to {destination_dir}")
    
def delete_pointed_files(file_path):
    try:
        os.remove(file_path)
    except OSError as e:
        print(f"An error occurred while deleting the file {file_path}")
        print("Error code:", e.errno)
        clean_before_fatal_exit()
    print(f"Successfully deleted the file {file_path}")

def clean_before_fatal_exit():
    print("Process finished with a fatal error, cleaning up temporary files located in", TEMP_DIR)
    shutil.rmtree(TEMP_DIR)
    sys.exit(1)

if __name__ == "__main__":
    if '-h' in sys.argv or '--help' in sys.argv:
        print("Usage: python validate_diffs.py -r <repository_name> -p <patch_dir> [-v] [-k]")
        print("Example Usage: python validate_diffs.py -r pokeyellow -p ./pokeyellow -v")
        print("Options:")
        print("  -r, --repository_name   Name of the repository of the original game")
        print("  -p, --patch_dir         Path for the directory where the patch files are stored (default:" + os.path.join(os.getcwd(),'diffs') + ")")
        print("  -k, --keep_dir          Keep the directory with the compiled modified game")
        print("  -v, --verbose           Make the script output more verbose")
        print("Supported Repositories:")
        for name, url in SUPPORTED_REPOSITORIES.items():
            print(f"  {name}: {url}")
    else:
        repository_name, patch_dir, keep_dir, verbose = parse_arguments()
        build_modified_structure(repository_name, patch_dir, keep_dir, verbose)

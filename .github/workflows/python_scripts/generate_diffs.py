import os
import shutil
import sys
import argparse
import subprocess
from pathlib import Path
from urllib.parse import urlparse

SUPPORTED_EXTENSIONS = ['asm']
SUPPORTED_REPOSITORIES = {'pokeyellow': "https://github.com/pret/pokeyellow.git", 'pokecrystal': "https://github.com/pret/pokecrystal.git"}
TEMP_DIR = Path('/tmp/temp_clone')

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="""Compares the directories of the original game, where the original directory is the cloned repository of the unmodified game,
        and the new directory, where all the desired modifications of the game have been implemented on top of the original directory structure.
        It then will generate a patch file for each file that is different from the original. These patch files will be created in a new folder called diffs, which will be placed in the current directory.
        Make sure that the directory with the modified game has the same folder structure as the original. If you have compiled the game at least once in the directory with your
        modifications, use the flag -c or --compiled.
        Any new files created in the new directory will be directly copied to the patch directory, and any files from the original directory that are deleted the new directory
        will be saved in the patch directory as empty *.delete files. All these files will be used in a GitHub workflow to compile the game with your changes, so make sure 
        that the compilation works."""
    )
    
    parser.add_argument('-r', '--repository_name', required=True, help='Name of the repository of the original game, use --help to see the list of supported games')
    parser.add_argument('-m', '--modified_dir', required=True, help='Path to the directory with the modified game')
    parser.add_argument('-c', '--compiled', action='store_true', help='Indicate that the directory with the modified game has been compiled at least once')
    parser.add_argument('-e', '--extensions', default=','.join(SUPPORTED_EXTENSIONS), help=f"Comma-separated list of file extensions to consider. Default: {', '.join(SUPPORTED_EXTENSIONS)}")
    parser.add_argument('-v', '--verbose', action='store_true', help='Make the script output more verbose (default: not verbose)')
    
    args = parser.parse_args()

    if args.extensions:
        extensions = args.extensions.split(',')
        for ext in extensions:
            if ext not in SUPPORTED_EXTENSIONS:
                parser.error(f"Extension '{ext}' is not supported. Supported extensions are: {', '.join(SUPPORTED_EXTENSIONS)}")
    else:
        extensions = SUPPORTED_EXTENSIONS
        
    if not os.path.isabs(args.modified_dir):
        args.modified_dir = os.path.join(os.getcwd(), args.modified_dir)

    return args.repository_name, args.modified_dir, args.compiled, extensions, args.verbose

def compare_and_generate_patches(repo_name, modified_dir, compiled, extensions, verbose):
    patch_dir = os.path.join(os.getcwd(),'diffs')
    patch_dir.mkdir(parents=True, exist_ok=True)
    original_dir = Path(clone_game_repo(repo_name, verbose))
    modified_dir = Path(modified_dir)
    if compiled:
        compile_cloned_game(original_dir)
    
    print("Original directory:", original_dir)
    print("Modified directory:", modified_dir)
    print("Patch directory:", patch_dir)

    for dirpath, _, filenames in os.walk(original_dir):
        print("Scanning directory:", dirpath)
        if verbose:
            print("Files found:", filenames)
        for filename in filenames:
            if verbose:
                print("Scanning file:", filename)
            if filename.split('.')[-1] not in extensions:
                if verbose:
                    print("Skipping file with unsupported extension:", filename)
                continue
            
            original_file = Path(dirpath) / filename
            relative_path = original_file.relative_to(original_dir)
            new_file = modified_dir / relative_path
            
            if verbose:
                print("Original file:", original_file)
                print("Relative path:", relative_path)
                print("New file:", new_file)
            
            if new_file.exists():
                if verbose:
                    print("New file exists:", new_file)
                if not files_are_identical(original_file, new_file):
                    print("Found modified file:", new_file)
                    patch_file = patch_dir / relative_path.with_name(relative_path.name + '.patch')
                    patch_file.parent.mkdir(parents=True, exist_ok=True)
                    if verbose:
                        print("Generating patch file:", patch_file)
                    generate_patch(original_file, new_file, patch_file)
            else:
                print("New file does not exist:", new_file)
                delete_file = patch_dir / relative_path.with_name(relative_path.name + '.delete')
                delete_file.parent.mkdir(parents=True, exist_ok=True)
                delete_file.touch()
                print("Created empty .delete file:", delete_file)

    for dirpath, _, filenames in os.walk(modified_dir):
        print("Scanning directory:", dirpath)
        if verbose:
            print("Files found:", filenames)
        for filename in filenames:
            if verbose:
                print("Scanning file:", filename)
            if filename.split('.')[-1] not in extensions:
                if verbose:
                    print("Skipping file with unsupported extension:", filename)
                continue
            
            new_file = Path(dirpath) / filename
            relative_path = new_file.relative_to(modified_dir)
            original_file = original_dir / relative_path
            if verbose:
                print("Original file:", original_file)
                print("Relative path:", relative_path)
                print("New file:", new_file)
            
            if not original_file.exists():
                print("Original file does not exist:", original_file)
                copy_to_patch_dir = patch_dir / relative_path
                copy_to_patch_dir.parent.mkdir(parents=True, exist_ok=True)
                copy_to_patch_dir.write_bytes(new_file.read_bytes())
                print("Copied new file to patch directory:", copy_to_patch_dir)
    
    print("Process finished successfully, cleaning up temporary files located in", TEMP_DIR)
    shutil.rmtree(TEMP_DIR)

def files_are_identical(file1, file2):
    if verbose:
        print("Comparing files:", file1, "and", file2)
    are_identical = file1.read_bytes() == file2.read_bytes()
    if verbose:
        if are_identical:
            print("Files are identical")
        else:
            print("Files are not identical")
    return are_identical

def generate_patch(original_file, new_file, patch_file):
    try:
        with open(patch_file, 'w') as patch_output:
            subprocess.run(['diff', str(original_file), str(new_file)], stdout=patch_output, check=True)
    except subprocess.CalledProcessError as e:
        # The diff binary has 3 possible return codes: 0 if the files are identical, 1 if they are different, and 2 if an error occurred.
        if e.returncode == 2:
            print(f"An error occurred while generating the patch {patch_file} from the differences between {original_file} and {new_file}")
            print("Output:", e.stderr)
            print("Return Code:", e.returncode)
            clean_before_fatal_exit()
        elif e.returncode == 1:
            print("Successfully generated patch file:", patch_file)
        else: # e.returncode == 0
            # This should never happen as we verified earlier that the files were different.
            print("The files are identical.")
            if patch_file.exists():
                patch_file.unlink()

def clone_game_repo(repo_name,verbose=False):
    github_url = SUPPORTED_REPOSITORIES[repo_name]
    print("Cloning repository:", github_url)
    # Before running this process, move the current directory to /tmp, create a dir called 'temp_clone', and clone the repo in there.
    if not TEMP_DIR.exists():
        TEMP_DIR.mkdir()
    if verbose:
        print("Temporary clone directory:", TEMP_DIR)
    os.chdir(TEMP_DIR)
    if verbose:
        print("Current working directory:", os.getcwd())
    try:
        subprocess.run(['git', 'clone', github_url], check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print("An error occurred while cloning the repository.")
        print("Output:", e.stderr)
        print("Return Code:", e.returncode)
        clean_before_fatal_exit()
    print("Repository cloned successfully.")
    return os.path.join(TEMP_DIR, repo_name)

def compile_cloned_game(dir):
    os.chdir(dir)
    try:
        subprocess.run(['make'], check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print("An error occurred while compiling the game.")
        print("Output:", e.stderr)
        print("Return Code:", e.returncode)
        clean_before_fatal_exit()
    print("Compilation finished successfully.")

def clean_before_fatal_exit():
    print("Process finished with a fatal error, cleaning up temporary files located in", TEMP_DIR)
    shutil.rmtree(TEMP_DIR)
    sys.exit(1)
        
if __name__ == "__main__":
    if '-h' in sys.argv or '--help' in sys.argv:
        print("Usage: python generate_diffs.py -r <repository_name> -m <modified_dir> [-e <extensions>] [-v] [-c]")
        print("Example Usage: python generate_diffs.py -r pokeyellow -m ./pokeyellow -c -v")
        print("Options:")
        print("  -r, --repository_name   Name of the repository of the original game")
        print("  -m, --modified_dir      Path to the directory with the modified game")
        print("  -c, --compiled          Indicate that the directory with the modified game has been compiled at least once. If you select this flag, make sure that your system still has all the dependencies needed to compile the project, but since you did compile it to need to mark this flag, you probably do.")
        print("  -e, --extensions        Comma-separated list of file extensions to consider (default: Everything within the Supported Extensions)")
        print("  -v, --verbose           Make the script output more verbose")
        print("Will generate all the patches in a directory structure located in ./diffs")
        print("Supported Extensions:" + ", ".join(SUPPORTED_EXTENSIONS))
        print("Supported Repositories:")
        for name, url in SUPPORTED_REPOSITORIES.items():
            print(f"  {name}: {url}")
    else:
        repository_name, modified_dir, compiled, extensions, verbose = parse_arguments()
        compare_and_generate_patches(repository_name, modified_dir, compiled, extensions, verbose)

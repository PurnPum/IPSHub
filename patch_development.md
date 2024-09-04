### Steps to implement a new patch into the system

1. **Clone the repository of the game you're implementing this feature for**
   - Here is the list of the currently supported games:
      - [Pokemon: Yellow Edition](https://github.com/pret/pokeyellow)
      - [Pokemon: Crystal Edition](https://github.com/pret/pokecrystal)

2. **Modify the files that you consider to implement your idea**
   - For now, only assembly (.asm) files are being supported, so no image/sound modifications yet.
   - Do __not__ modify any filenames if possible, the script will still work, but it will take longer and will create a more convoluted and inefficient structure.

3. **Once finished, generate the structure of .patch files using the provided python script.**
   - The python script resides in the root of the repository, the file being __generate_diffs.py__
   - Here is the script usage output (from using the -h or --help flags):
     ```
     Usage: python generate_diffs.py -r <repository_name> -m <modified_dir> [-e <extensions>] [-p <patch_dir>] [-v] [-c]
     Example Usage: python generate_diffs.py -r pokeyellow -m ./pokeyellow -c -v
     Options:
       -r, --repository_name   Name of the repository of the original game
       -m, --modified_dir      Path to the directory with the modified game
       -c, --compiled          Indicate that the directory with the modified game has been compiled at least once. If you select this flag, make sure that your system still has all the dependencies needed to compile the project, but since you did compile it to need to mark this flag, you probably do.
       -e, --extensions        Comma-separated list of file extensions to consider (default: Everything within the Supported Extensions)
       -p, --patch_dir         Path for the directory to store patch files (default:./diffs)
       -v, --verbose           Make the script output more verbose
     Supported Extensions:asm
     Supported Repositories:
       pokeyellow: https://github.com/pret/pokeyellow.git
       pokecrystal: https://github.com/pret/pokecrystal.git
     ```
   - Make sure to use the exact word for the repository_name, those are provided on the __Supported Repositories__ section from the usage output.
   - The __-c__ flag is very important if you have compiled the game at least once in the directory that you're going to pass as the modified_dir, which is very likely. If you did compile its very likely that your system still has all the tools/dependencies installed, but still make sure you do. Refer to the install.md file on the repositories of the games.
   - If you run the script with increased verbosity (-v), its recommended to pipe the standard output to a log file, otherwise most of it will be cut-off from the shell.
   - This script uses various libraries that you can check at the beggining of the file, all of them should be installed by default on a modern python 3.x installation.
   - The script clones the repository in a folder in /tmp/, make sure there is public access to that directory (which there should be by default)
   - Once the script finished successfully, you will have a structure of directories in ./diffs (or somewhere else if you used the -p flag). The content of this structure is as follows:
      - For every file that has been modified, a .patch file with the same filename and suffix as the original file will take its place (for example main.asm.patch)
      - For every file that has been removed, an empty .delete file with the same filename and suffix as the original file will take its place (for example main.asm.delete)
      - For every new file that has been added, it will be copied directly to its corresponding directory.
   - You can verify that all the files are in their proper place by running the __tree__ binary pointing to the directory with the patches. (It needs to be installed externally)
     ```bash
     tree .diffs
     ```

	 
	 # TODO: seguir con este .md de comentario para una issue de desarrollo para user
	 # TODO: en la del equipo poner la branch y este md pero por defecto escondido.
	 # TODO: Después revisar lo del script que genere los .patch, así el user no lo tiene que hacer él.
	 # TODO: Añadir workflow en la Pull Request que simplemente valide que la ROM compila
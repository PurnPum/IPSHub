# IPSHub
Main repository for the web service used by IPSHub.org

This project is for an online ROM patching web service, which will allow anyone to customize a ROM that they own with multiple configurations that can be selected from the website interface. Do you want to quickly get a patch for a Pokemon Crystal ROM so that your starters are changed, while also randomizing the map warps, making the AI more difficult and forcing nuzlocke rules?

You'll very easily be able to do that once this project is completed, you'll still need the original ROM that needs to be patched, since we're not distributing any ROMs directly.

Once the entire web service is implemented and running, users will be able to create pull requests to add more implementations for patching, instructions will be added once that system is built, it will rely very heavily on GitHub Actions for system and file validation.

## HOW TO RUN THE WEBSITE LOCALLY:

First, clone the repository:

```bash
git clone https://github.com/PurnPum/IPSHub.git
```

Next, place yourself on the root of the project, and create the docker image:

```bash
sudo docker build -t <image_name> .
```

Finally, run the container:

```bash
sudo docker run -p 8000:8000 <image_name>
```

Now you can visit the website at http://localhost:8000
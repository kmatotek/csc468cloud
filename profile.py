import geni.portal as portal
import geni.rspec.pg as rspec

# Create a Portal context.
pc = portal.Context()

# Define parameters for storage and Git repo.
pc.defineParameter("datasetType", "Dataset type (persistent or local)", 
                   portal.ParameterType.STRING, "local")
pc.defineParameter("datasetURN", "If persistent, provide Image-backed Dataset URN", 
                   portal.ParameterType.STRING, "urn:publicid:IDN+emulab.net:testbed+imdataset+example")
pc.defineParameter("mountPoint", "Mount point for dataset", 
                   portal.ParameterType.STRING, "/mydata")
pc.defineParameter("gitRepo", "Git repository SSH URL", 
                   portal.ParameterType.STRING, "git@github.com:yourusername/yourrepo.git")

params = pc.bindParameters()

# Create an RSpec request object.
request = pc.makeRequestRSpec()

# Create a RawPC node with Ubuntu 22.04.
node = request.RawPC("node")
node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"

# Attach storage:
# If the user selects persistent storage, attach an image-backed dataset.
# Otherwise, attach a local (ephemeral) dataset of 30GB.
if params.datasetType.lower() == "persistent":
    bs = node.Blockstore("bs", params.mountPoint)
    bs.dataset = params.datasetURN
else:
    bs = node.Blockstore("bs", params.mountPoint)
    bs.size = "30GB"

# Create a startup script that:
# 1. Installs Git.
# 2. Clones the Git repository (if not already cloned) into the dataset mountpoint.
# 3. Runs your program (here simulated by writing a file with a timestamp).
# 4. Adds, commits, and pushes the changes back to the repository.
command = f"""#!/bin/bash
sudo apt update && sudo apt install -y git
cd {params.mountPoint}
if [ ! -d repo ]; then
    git clone {params.gitRepo} repo
fi
cd repo
# Simulate program execution by creating an output file with a timestamp.
echo "Data generated at $(date)" > output_$(date +%s).txt
git add .
git commit -m "Automated commit: $(date)"
git push
"""

# Attach the startup script to the node.
node.addService(rspec.Execute(shell="/bin/bash", command=command))

# Print the RSpec so that CloudLab can instantiate the experiment.
pc.printRequestRSpec(request)

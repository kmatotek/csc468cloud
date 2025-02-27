import geni.portal as portal
import geni.rspec.pg as rspec

pc = portal.Context()

# Define parameters for storage, repository URL, and program entry command.
pc.defineParameter("datasetType", "Dataset type (persistent or local)", 
                   portal.ParameterType.STRING, "local")
pc.defineParameter("datasetURN", "If persistent, provide Image-backed Dataset URN", 
                   portal.ParameterType.STRING, "urn:publicid:IDN+emulab.net:testbed+imdataset+example")
pc.defineParameter("mountPoint", "Mount point for dataset", 
                   portal.ParameterType.STRING, "/mydata")
pc.defineParameter("gitRepo", "Git repository SSH URL", 
                   portal.ParameterType.STRING, "git@github.com:yourusername/yourrepo.git")
pc.defineParameter("entryCommand", "Command to execute your program (e.g., 'python3 run_experiment.py')", 
                   portal.ParameterType.STRING, "python3 run_experiment.py")

params = pc.bindParameters()

# Create the RSpec request object.
request = pc.makeRequestRSpec()

# Allocate a RawPC node with an Ubuntu 22.04 image.
node = request.RawPC("node")
node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"

# Attach storage:
# Use a persistent (image-backed) dataset if requested, otherwise use a local ephemeral dataset.
if params.datasetType.lower() == "persistent":
    bs = node.Blockstore("bs", params.mountPoint)
    bs.dataset = params.datasetURN
else:
    bs = node.Blockstore("bs", params.mountPoint)
    bs.size = "30GB"

# Startup script:
# 1. Update packages and install Git and Python3.
# 2. Go to the mount point.
# 3. Clone the repo if it hasn't been cloned already.
# 4. Change into the repository directory.
# 5. Execute your program via the provided command.
# 6. Commit any changes and push them back to GitHub.
command = f"""#!/bin/bash
# Update packages and install required software.
sudo apt update && sudo apt install -y git python3

# Change to the mounted storage.
cd {params.mountPoint}

# Clone the repository if it doesn't already exist.
if [ ! -d repo ]; then
    git clone {params.gitRepo} repo
fi

cd repo

# Execute your program (this should generate output files, etc.).
{params.entryCommand}

# Add all changes, commit, and push them to the repository.
git add .
# Commit only if there are changes.
git commit -m "Automated commit from CloudLab: $(date)" || echo "No changes to commit"
git push origin main
"""

# Attach the startup script to be executed when the node boots.
node.addService(rspec.Execute(shell="/bin/bash", command=command))

# Output the RSpec to CloudLab.
pc.printRequestRSpec(request)

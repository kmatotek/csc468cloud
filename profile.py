import geni.portal as portal
import geni.rspec.pg as rspec
import geni.rspec.emulab

# Create a Request object to start building the RSpec.
request = portal.context.makeRequestRSpec()

# Allocate a node and force it to be of the 'nvidiagh' type (with NVIDIA Hopper GPU).
node = request.RawPC("node")
node.hardware_type = "nvidiagh"  # Ensure you're allocated a node with the NVIDIA H100 (Hopper) GPU

# Configure the node's resources.
node.cores = 72          # 72-core CPU (Arm Neoverse V2)
node.ram = 480000        # 480GB RAM (in MB)
node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU20-64-STD"  # Confirm this image is available

# Optionally, add services to update and install packages.
node.addService(rspec.Execute(shell="bash", command="echo Using GPU"))
node.addService(rspec.Execute(shell="/bin/sh", command="sudo apt update"))
node.addService(rspec.Execute(shell="/bin/sh", command="sudo apt install -y git python3 apache2"))
node.addService(rspec.Execute(shell="/bin/sh", command='sudo systemctl status apache2'))

# Allocate NVMe storage at /mydata.
bs = node.Blockstore("bs", "/mydata")
bs.size = 1000  # Size in GB (i.e. 1000GB)

# Add a network interface.
node.addInterface("eth0")

# Print the RSpec to the enclosing page.
portal.context.printRequestRSpec()

import geni.portal as portal
import geni.rspec.pg as rspec
import geni.rspec.emulab

# Create a Request object to start building the RSpec.
request = portal.context.makeRequestRSpec()


# Allocate a node with the correct hardware configuration.
node = request.RawPC("node")
node.hardware_type = "nvidiagh"
node.cores = 72  # 72-core CPU (Arm Neoverse V2)
node.ram = 480000  # 480GB RAM (in MB)
node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU20-64-STD"  # Make sure this image is available for nvidiagh

# Specify the GPU (NVIDIA H100) if needed for your tasks. This will depend on your usage.
node.addService(rspec.Execute(shell="bash", command="echo Using GPU"))
node.addService(rspec.Execute(shell="/bin/sh", command="sudo apt update"))
node.addService(rspec.Execute(shell="/bin/sh", command="sudo apt install -y git python3 apache2"))
node.addService(rspec.Execute(shell="/bin/sh", command='sudo systemctl status apache2'))

# Allocate NVMe storage. One 1.9TB SSD and one 960GB SSD.

bs = node.Blockstore("bs", "/mydata")
bs.size = "1000GB"  # 1 tb

# Set networking options if relevant (e.g., Mellanox ConnectX-7 100Gbps NIC)
node.addInterface("eth0")

# Print the RSpec to the enclosing page.
portal.context.printRequestRSpec()

import geni.portal as portal
import geni.rspec.pg as rspec
import geni.rspec.emulab

# Create a Request object to start building the RSpec.
request = portal.context.makeRequestRSpec()

# Allocate a node and request a blockstore (disk) of 400GB mounted at /mydata.
node = request.RawPC("node")
node.cores = 4
node.ram = 4096
node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU16-64-STD"  # Use a suitable image
bs = node.Blockstore("bs", "/mydata")
bs.size = "500GB"  # Size of the blockstore

# Print the RSpec to the enclosing page.
portal.context.printRequestRSpec()

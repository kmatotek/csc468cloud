import geni.portal as portal
import geni.rspec.pg as rspec

pc = portal.Context()
request = pc.makeRequestRSpec()

# Allocate a simple node
node = request.RawPC("node")
node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"

pc.printRequestRSpec(request)

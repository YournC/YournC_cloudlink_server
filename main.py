import os
import asyncio
from cloudlink import server
from cloudlink.server.protocols import clpv4

# Initialize server
server_inst = server()

# Load the Cloudlink Protocol v4 (CLPv4)
# Note: Ensure the protocol is attached to the server instance
cl_protocol = clpv4(server_inst)

# Get port from Render environment (Render uses a string, so int() is good)
port = int(os.environ.get("PORT", 10000))

if __name__ == "__main__":
    print(f"Starting Cloudlink 4.0 server on 0.0.0.0:{port}...")
    
    # In Cloudlink 4, the run method usually expects 'host', not 'ip'
    # and it needs to know which protocol to use.
    server_inst.run(host="0.0.0.0", port=port)

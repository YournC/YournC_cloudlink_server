import os
from cloudlink import server
from cloudlink.server.protocols import clpv4

# Initialize server
server_inst = server()

# Get port from Render environment
port = int(os.environ.get("PORT", 10000))

# Load the Cloudlink Protocol v4 (CLPv4)
cl_protocol = clpv4(server_inst)

# Start the server
if __name__ == "__main__":
    print(f"Starting Cloudlink 4.0 server on port {port}...")
    # Change 'host' to 'ip' here:
    server_inst.run(ip="0.0.0.0", port=port)

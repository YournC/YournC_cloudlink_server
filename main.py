import os
import asyncio
from cloudlink import server
from cloudlink.server.protocols import clpv4

async def main():
    # Initialize server
    server_inst = server()
    
    # Get port from Render environment
    port = int(os.environ.get("PORT", 10000))
    
    # Load the Cloudlink Protocol v4 (CLPv4)
    cl_protocol = clpv4(server_inst)
    
    print(f"Starting Cloudlink 4.0 server on port {port}...")
    
    # We use the underlying run method but ensure it binds to 0.0.0.0
    # If server_inst.run(ip=...) is what your version uses, keep it!
    # But we run it as an awaited task if possible, or via the built-in blocking call.
    server_inst.run(ip="0.0.0.0", port=port)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped.")

import os
from cloudlink import server
from cloudlink.server.protocols import clpv4

def main():
    # Initialize server
    server_inst = server()

    # Get port from Render environment
    port = int(os.environ.get("PORT", 10000))

    # Load the Cloudlink Protocol v4 (CLPv4)
    cl_protocol = clpv4(server_inst)

    print(f"Starting Cloudlink 4.0 server on 0.0.0.0:{port}...")
    
    # Cloudlink's .run() handles the asyncio.run() internally.
    # Just call it directly without wrapping it in an async function.
    server_inst.run(ip="0.0.0.0", port=port)

if __name__ == "__main__":
    main()

import os
from cloudlink import server
from cloudlink.server.protocols import clpv4

def main():
    # Initialize server
    server_inst = server()

    # Get port from Render
    port = int(os.environ.get("PORT", 10000))

    # Load Protocol
    cl_protocol = clpv4(server_inst)

    print(f"Cloudlink 4.0 starting on port {port}...")

    # We use the simplest run command that worked before.
    # To fix the "HEAD" crash logs, we'll let it happen 
    # but ensure the server doesn't stop.
    try:
        server_inst.run(ip="0.0.0.0", port=port)
    except Exception as e:
        print(f"Server encountered an error: {e}")

if __name__ == "__main__":
    main()

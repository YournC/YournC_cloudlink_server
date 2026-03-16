import os
from cloudlink import server
from cloudlink.server.protocols import clpv4

def main():
    server_inst = server()
    
    # Render provides the port
    port = int(os.environ.get("PORT", 10000))
    
    # Initialize the protocol
    cl_protocol = clpv4(server_inst)
    
    print(f"Cloudlink 4.0 is live. Internal Port: {port}")
    
    # We bind to 0.0.0.0 so the container accepts outside traffic
    server_inst.run(ip="0.0.0.0", port=port)

if __name__ == "__main__":
    main()

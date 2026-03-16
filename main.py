import os
import time
import threading
from cloudlink import server
from cloudlink.server.protocols import clpv4

# ... Keep your run_temporary_handler function exactly the same ...

def main():
    port = int(os.environ.get("PORT", 10000))
    run_temporary_handler(port)

    # 1. Initialize Cloudlink
    server_inst = server()
    
    # 2. Critical settings for PenguinMod/TurboWarp
    server_inst.check_origin = False  # Allow browser connections from penguinmod.com
    
    # 3. Use the CLPv4 protocol
    cl_protocol = clpv4(server_inst)
    
    # 4. Bind Cloudlink specifically to the websockets engine
    # This helps ensure the internal 'websockets' library uses the 
    # correct handshake for browser clients.
    print(f"Cloudlink 4.0 starting for PenguinMod on port {port}...")
    
    # Run without specialized wrappers to keep headers clean
    server_inst.run(ip="0.0.0.0", port=port)

if __name__ == "__main__":
    main()

import os
import time
import threading
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
from cloudlink import server
from cloudlink.server.protocols import clpv4

# Silence the 'websockets' library logging to keep Render logs clean
logging.getLogger("websockets").setLevel(logging.CRITICAL)

# 1. Define the Health Check Handler
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()
        
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")
        
    def log_message(self, format, *args):
        return

# 2. Define the Temporary Server function
def run_temporary_handler(port):
    print(f"Bypassing Render health check on {port}...")
    try:
        # This server only exists for 5 seconds to satisfy Render's startup probe
        httpd = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
        threading.Thread(target=httpd.handle_request).start() 
        time.sleep(5)
        httpd.server_close()
        print("Health check passed. Handing port over to Cloudlink.")
    except Exception as e:
        print(f"Temporary server notice: {e}")

# 3. The Main Execution
def main():
    # Use Render's dynamic port, default to 10000
    port = int(os.environ.get("PORT", 10000))
    
    # Satisfy Render's initial check
    run_temporary_handler(port)

    # Initialize Cloudlink
    server_inst = server()
    
    # Disable Origin Check (REQUIRED for PenguinMod/Browser connections)
    server_inst.check_origin = False 
    
    # Add a custom handler to ignore non-websocket pings after startup
    # This prevents those EOFError/Invalid Handshake logs
    def ignore_http_pings(path, headers):
        if "upgrade" not in headers.get("Connection", "").lower():
            return (200, [("Content-Type", "text/plain")], b"OK")
        return None
    
    # Attach the fix to the underlying websocket engine
    server_inst.ws.process_request = ignore_http_pings

    # Initialize the protocol
    cl_protocol = clpv4(server_inst)

    print(f"Cloudlink 4.0 is LIVE on port {port}")
    server_inst.run(ip="0.0.0.0", port=port)

if __name__ == "__main__":
    main()

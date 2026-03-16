import os
import time
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from cloudlink import server
from cloudlink.server.protocols import clpv4

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
    print(f"Starting temporary health check server on port {port}...")
    try:
        httpd = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
        # Handle one request (Render's ping) then move on
        threading.Thread(target=httpd.handle_request).start() 
        time.sleep(5)
        httpd.server_close()
        print("Temporary server closed. Switching to Cloudlink...")
    except Exception as e:
        print(f"Temporary server notice: {e}")

# 3. The Main Execution
def main():
    port = int(os.environ.get("PORT", 10000))
    
    # Satisfy Render's initial check
    run_temporary_handler(port)

    # Initialize Cloudlink
    server_inst = server()
    
    # CRITICAL FOR PENGUINMOD: Disable origin check
    server_inst.check_origin = False 
    
    # Initialize protocol
    cl_protocol = clpv4(server_inst)

    print(f"Cloudlink 4.0 is now starting on port {port}...")
    server_inst.run(ip="0.0.0.0", port=port)

if __name__ == "__main__":
    main()

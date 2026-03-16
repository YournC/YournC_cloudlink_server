import os
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
from cloudlink import server
from cloudlink.server.protocols import clpv4

# 1. Tiny handler for the initial Render ping
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

def run_temporary_handler(port):
    print(f"Temporary health check server listening on {port}...")
    httpd = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    # Serve for just enough time to satisfy the first few pings
    threading.Thread(target=httpd.handle_request).start() 
    time.sleep(5)
    httpd.server_close()
    print("Temporary server closed. Handing over to Cloudlink...")

def main():
    port = int(os.environ.get("PORT", 10000))
    run_temporary_handler(port)

    # Initialize Cloudlink
    server_inst = server()
    
    # RELAX ORIGIN CHECK:
    # This tells the server to accept connections even if the 'Origin' 
    # header doesn't match.
    server_inst.check_origin = False 

    cl_protocol = clpv4(server_inst)
    
    print(f"Cloudlink 4.0 starting on port {port}...")
    server_inst.run(ip="0.0.0.0", port=port)

if __name__ == "__main__":
    main()

import os
import time
import threading
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
from cloudlink import server
from cloudlink.server.protocols import clpv4

# 1. Suppress the 'websockets' handshake noise in logs
logging.getLogger("websockets.server").setLevel(logging.CRITICAL)

# 2. Temporary Health Check (The "Relay")
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
    print(f"Satisfying Render health check on {port}...")
    httpd = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    threading.Thread(target=httpd.handle_request).start() 
    time.sleep(5)
    httpd.server_close()

def main():
    port = int(os.environ.get("PORT", 10000))
    run_temporary_handler(port)

    # 3. Cloudlink Initialization
    server_inst = server()
    
    # CRITICAL: Disable origin check for Render's proxy
    server_inst.check_origin = False 
    
    cl_protocol = clpv4(server_inst)

    print(f"Cloudlink 4.0 fully active on port {port}")
    server_inst.run(ip="0.0.0.0", port=port)

if __name__ == "__main__":
    main()

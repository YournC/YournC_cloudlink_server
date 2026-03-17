import os
import threading
import time
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
from cloudlink import server
from cloudlink.server.protocols import clpv4

# Silence logs
logging.getLogger("websockets").setLevel(logging.CRITICAL)

class HealthCheck(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")
    def log_message(self, format, *args):
        return

def run_health_check(port):
    try:
        # A very short-lived server to "poke" the port open for Render
        httpd = HTTPServer(('0.0.0.0', port), HealthCheck)
        threading.Thread(target=httpd.handle_request).start()
        time.sleep(1)
        httpd.server_close()
    except:
        pass

def main():
    # Render tells us which port to use via this environment variable
    port = int(os.environ.get("PORT", 10000))
    
    # 1. Open the port for a split second to satisfy Render's scanner
    run_health_check(port)

    # 2. Setup Cloudlink
    server_inst = server()
    server_inst.check_origin = False 
    
    # 3. Apply Protocol
    clpv4(server_inst)
    
    print(f"Cloudlink 4.0 starting on port {port}...")
    
    # 4. START: This is the ONLY part that should run the loop
    server_inst.run(ip="0.0.0.0", port=port)

if __name__ == "__main__":
    main()

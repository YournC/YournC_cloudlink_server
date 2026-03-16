import os
import time
import threading
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
from cloudlink import server
from cloudlink.server.protocols import clpv4

# Silence the 'websockets' library logging to keep Render logs clean
logging.getLogger("websockets").setLevel(logging.CRITICAL)

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
    print(f"Bypassing Render health check on {port}...")
    try:
        httpd = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
        threading.Thread(target=httpd.handle_request).start() 
        time.sleep(5)
        httpd.server_close()
    except:
        pass

def main():
    port = int(os.environ.get("PORT", 10000))
    run_temporary_handler(port)

    # Initialize Cloudlink
    server_inst = server()
    
    # 1. Disable Origin Check (REQUIRED for PenguinMod)
    server_inst.check_origin = False 
    
    # 2. Add a custom handler to ignore non-websocket pings after startup
    def ignore_http_pings(path, headers):
        if "upgrade" not in headers.get("Connection", "").lower():
            return (200, [], b"OK") # Tell Render we are alive without crashing
        return None # Continue with normal WebSocket handshake
    
    # Apply the fix to the underlying websocket engine
    server_inst.ws.process_request = ignore_http_pings

    cl_protocol = clpv4(server_inst)
    print(f"Cloudlink 4.0 is LIVE for PenguinMod on port {port}")
    server_inst.run(ip="0.0.0.0", port=port)

if __name__ == "__main__":
    main()

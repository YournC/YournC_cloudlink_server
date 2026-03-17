import os
import time
import threading
import logging
import asyncio
from http.server import BaseHTTPRequestHandler, HTTPServer
from cloudlink import server
from cloudlink.server.protocols import clpv4

# Silence the 'websockets' library to clean up logs
logging.getLogger("websockets").setLevel(logging.CRITICAL)

class HealthCheckHandler(BaseHTTPRequestHandler):
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
    
    # 1. ALLOW ALL ORIGINS (Crucial for PenguinMod)
    server_inst.check_origin = False 
    
    # 2. Force the server to accept the Render Proxy headers
    # We override the process_request to handle pings and browser headers
    async def process_request(self, path, request_headers):
        # If it's a health check/ping from Render, return 200 OK
        if "upgrade" not in request_headers.get("Connection", "").lower():
            return (200, [], b"OK\n")
        return None

    # Apply the patch directly to the underlying engine
    server_inst.ws.process_request = process_request

    # 3. Use CLPv4
    cl_protocol = clpv4(server_inst)

    print(f"Cloudlink 4.0 is LIVE. Target URL: wss://yournc-cloudlink-server.onrender.com")
    
    # Run the server
    server_inst.run(ip="0.0.0.0", port=port)

if __name__ == "__main__":
    main()

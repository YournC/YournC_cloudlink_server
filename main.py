import os
import asyncio
import logging
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from cloudlink import server
from cloudlink.server.protocols import clpv4

# Silence all websockets logging to stop the log spam
logging.getLogger("websockets").setLevel(logging.CRITICAL)

# 1. Simple Health Check for Render's Startup
class HealthCheck(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")
    def log_message(self, format, *args):
        return

def run_health_check(port):
    httpd = HTTPServer(('0.0.0.0', port), HealthCheck)
    # Just handle one or two requests then close
    threading.Thread(target=httpd.handle_request).start()
    time.sleep(2)
    httpd.server_close()

async def start_cloudlink():
    port = int(os.environ.get("PORT", 10000))
    
    # Run a quick HTTP server to let Render know we are here
    run_health_check(port)

    # Initialize Cloudlink
    server_inst = server()
    server_inst.check_origin = False # Mandatory for PenguinMod
    
    # Custom Handshake Handler to ignore Render's pings without crashing
    async def process_request(path, request_headers):
        if "upgrade" not in request_headers.get("Connection", "").lower():
            return (200, [("Content-Type", "text/plain")], b"OK\n")
        return None

    # Apply the protocol
    clpv4(server_inst)
    
    print(f"Cloudlink 4.0 starting on port {port}...")
    
    # Start the server using the more stable manual method
    await server_inst.run(
        ip="0.0.0.0", 
        port=port, 
        process_request=process_request
    )

if __name__ == "__main__":
    asyncio.run(start_cloudlink())

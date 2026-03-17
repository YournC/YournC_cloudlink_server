import os
import asyncio
import logging
import threading
import time
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
        httpd = HTTPServer(('0.0.0.0', port), HealthCheck)
        threading.Thread(target=httpd.handle_request).start()
        time.sleep(2)
        httpd.server_close()
    except:
        pass

async def start_cloudlink():
    port = int(os.environ.get("PORT", 10000))
    
    # 1. Satisfy Render
    run_health_check(port)

    # 2. Setup Cloudlink
    server_inst = server()
    server_inst.check_origin = False # Fix for PenguinMod
    
    # 3. Apply Protocol
    clpv4(server_inst)
    
    print(f"Cloudlink 4.0 starting on port {port}...")
    
    # 4. Use the standard run method (no extra arguments)
    server_inst.run(ip="0.0.0.0", port=port)

if __name__ == "__main__":
    asyncio.run(start_cloudlink())

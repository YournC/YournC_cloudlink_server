import os
import asyncio
import http
from cloudlink import server
from cloudlink.server.protocols import clpv4

# This function prevents the "HEAD" request crash
async def health_check(path, request_headers):
    if "upgrade" not in request_headers.get("Connection", "").lower():
        return http.HTTPStatus.OK, [], b"OK"
    return None

async def start_server():
    server_inst = server()
    port = int(os.environ.get("PORT", 10000))
    cl_protocol = clpv4(server_inst)
    
    print(f"Starting Cloudlink 4.0 on port {port}...")

    # We bypass the 'server_inst.run' wrapper to access the websocket settings directly
    # This allows us to use process_request without the TypeError
    async with server_inst.asyncio_server.serve(
        server_inst._server_loop, # The internal handler
        host="0.0.0.0",
        port=port,
        process_request=health_check
    ):
        await asyncio.Future() # Keep the server running forever

if __name__ == "__main__":
    try:
        asyncio.run(start_server())
    except KeyboardInterrupt:
        pass

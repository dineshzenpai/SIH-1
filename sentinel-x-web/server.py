"""Launch the dependency-free SENTINEL-X demo site on localhost."""

from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import sys


class SentinelHandler(SimpleHTTPRequestHandler):
    extensions_map = {
        **SimpleHTTPRequestHandler.extensions_map,
        ".html": "text/html; charset=utf-8",
        ".js": "text/javascript; charset=utf-8",
        ".css": "text/css; charset=utf-8",
    }


if __name__ == "__main__":
    root = Path(__file__).resolve().parent
    host = "127.0.0.1"
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    print("=" * 64)
    print("  SENTINEL-X | Identity Forensics Demo")
    print(f"  Local console: http://{host}:{port}")
    print("  Press Ctrl+C to stop the server")
    print("=" * 64)
    handler = lambda *args, **kwargs: SentinelHandler(*args, directory=str(root), **kwargs)
    ThreadingHTTPServer((host, port), handler).serve_forever()


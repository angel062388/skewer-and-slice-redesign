# Local-only receiver: the browser POSTs a base64 image, it lands in mockup/assets.
import http.server, base64, sys, os
ROOT = sys.argv[1]
class H(http.server.BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', '*')
    def do_OPTIONS(self):
        self.send_response(204); self._cors(); self.end_headers()
    def do_POST(self):
        n = int(self.headers.get('Content-Length', 0)); body = self.rfile.read(n)
        name = os.path.basename(self.path.strip('/'))
        if not name.endswith(('.jpg', '.png', '.webp')):
            self.send_response(400); self._cors(); self.end_headers(); return
        data = base64.b64decode(body.split(b',', 1)[-1])
        with open(os.path.join(ROOT, name), 'wb') as f: f.write(data)
        self.send_response(200); self._cors(); self.send_header('Content-Type', 'text/plain'); self.end_headers()
        self.wfile.write(str(len(data)).encode())
    def log_message(self, *a): pass
http.server.HTTPServer(('127.0.0.1', 8788), H).serve_forever()

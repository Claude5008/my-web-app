from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from datetime import datetime

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = f'''
            <!DOCTYPE html>
            <html>
            <head>
                <title>My Custom Docker App</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; background: #f0f0f0; }
                    .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                    h1 { color: #2c3e50; }
                    .info { background: #ecf0f1; padding: 15px; border-radius: 5px; margin: 20px 0; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🐳 Hello from My Custom Docker Container!</h1>
                    <div class="info">
                        <p><strong>Container ID:</strong> """ + open('/proc/self/cgroup').read().split('/')[-1][:12] + """</p>
                        <p><strong>Time:</strong> """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
                        <p><strong>Message:</strong> This is running inside a custom Docker image I built!</p>
                    </div>
                    <p>This web server is running Python inside a Docker container that I created from scratch.</p>
                    <p>Try visiting <a href="/api">/api</a> for JSON data.</p>
                </div>
            </body>
            </html>
            '''
            self.wfile.write(html.encode())
            
        elif self.path == '/api':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            data = {
                "message": "Hello from custom Docker API!",
                "timestamp": datetime.now().isoformat(),
                "container_info": "Running in custom Python container"
            }
            self.wfile.write(json.dumps(data, indent=2).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8000), RequestHandler)
    print("🚀 Server starting on port 8000...")
    server.serve_forever()
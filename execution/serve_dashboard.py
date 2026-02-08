import http.server
import socketserver
import os
import webbrowser
import json
import urllib.parse
from fetch_reddit_posts import fetch_and_score_posts

PORT = 8000
DIRECTORY = "." # Serve current directory

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        # Parse URL
        parsed_url = urllib.parse.urlparse(self.path)
        
        # API Endpoint: /api/fetch_topic?name=<subreddit>
        if parsed_url.path == "/api/fetch_topic":
            query_params = urllib.parse.parse_qs(parsed_url.query)
            topic = query_params.get("name", [""])[0]
            
            if not topic:
                self.send_error(400, "Missing 'name' parameter")
                return

            print(f"API Request: Fetching topic '{topic}'...")
            
            try:
                # Reuse the logic from our fetch script
                posts = fetch_and_score_posts(topic)
                
                # Send JSON response
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*") # CORS for dev
                self.end_headers()
                self.wfile.write(json.dumps(posts).encode('utf-8'))
                print(f"API Success: Sent {len(posts)} posts for '{topic}'")
                
            except Exception as e:
                print(f"API Error: {e}")
                self.send_error(500, str(e))
                
        else:
            # Default behavior for static files
            super().do_GET()

def main():
    print(f"Starting dashboard server at http://localhost:{PORT}/dashboard/")
    print("Press Ctrl+C to stop.")
    
    # Open browser automatically
    webbrowser.open(f"http://localhost:{PORT}/dashboard/")
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopping server...")
            httpd.server_close()

if __name__ == "__main__":
    main()

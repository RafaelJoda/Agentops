from http.server import BaseHTTPRequestHandler
import json
import os
import sys
from urllib import parse

# Add execution directory to path so we can import fetch_reddit_posts
sys.path.append(os.path.join(os.path.dirname(__file__), '../execution'))

try:
    from fetch_reddit_posts import fetch_and_score_posts
except ImportError:
    # Fallback/Mock if import fails in Vercel environment
    def fetch_and_score_posts(topic, limit=100, top_k=5):
        return []

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse query params
        url_components = parse.urlparse(self.path)
        query_params = parse.parse_qs(url_components.query)
        topic = query_params.get('name', [''])[0]

        if not topic:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Missing name parameter"}).encode('utf-8'))
            return

        try:
            # Fetch data
            posts = fetch_and_score_posts(topic)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(posts).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))

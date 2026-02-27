from http.server import BaseHTTPRequestHandler
import json
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/stats':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            try:
                from brain.master_mind import master_mind
                from brain.knowledge_engine import knowledge_engine
                
                stats = {
                    'consciousness': master_mind.consciousness['level'],
                    'books': len(knowledge_engine.books),
                    'dreams': len(master_mind.working_memory.get('dreams', [])),
                    'users': master_mind.stats['total_thoughts']
                }
            except:
                stats = {
                    'consciousness': 1.0,
                    'books': 4,
                    'dreams': 0,
                    'users': 0
                }
            
            self.wfile.write(json.dumps(stats).encode())
        else:
            self.send_response(404)
            self.end_headers()

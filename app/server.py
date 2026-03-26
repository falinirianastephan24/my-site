import http.server
import socketserver
import sqlite3
import os

# 1. Fikirana ny Port ho an'ny Render
PORT = int(os.environ.get("PORT", 8000))

# 2. Lalana (Paths) mankany amin'ny dossiers hafa
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
DB_PATH = os.path.join(os.path.dirname(__file__), 'database.db')

class MyHandler(http.server.SimpleHTTPRequestHandler):
    
    def do_GET(self):
        # A. Raha mangataka CSS (ao amin'ny /static/)
        if self.path.startswith('/static/'):
            try:
                file_name = self.path.split('/')[-1]
                file_path = os.path.join(STATIC_DIR, file_name)
                
                self.send_response(200)
                self.send_header('Content-type', 'text/css')
                self.end_headers()
                
                with open(file_path, 'rb') as f:
                    self.wfile.write(f.read())
            except Exception:
                self.send_error(404, "Tsy hita ny CSS")
            return

        # B. Pejy fandraisana (HTML + SQLite)
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()

            # --- DATABASE: Maka data ---
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS olona (anarana TEXT)")
            # Manampy ohatra raha mbola banga
            cursor.execute("SELECT COUNT(*) FROM olona")
            if cursor.fetchone()[0] == 0:
                cursor.execute("INSERT INTO olona VALUES ('Rakoto'), ('Rabe')")
                conn.commit()
            
            cursor.execute("SELECT anarana FROM olona")
            rows = cursor.fetchall()
            conn.close()

            # --- HTML: Mamaky sy mameno data ---
            html_file = os.path.join(TEMPLATE_DIR, 'index.html')
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Manolo ny {{data}} ho lisitra HTML
                data_list = "".join([f"<li>{r[0]}</li>" for r in rows])
                final_html = content.replace("{{data}}", data_list)
                
                self.wfile.write(bytes(final_html, "utf-8"))
            except FileNotFoundError:
                self.wfile.write(b"Tsy hita ny index.html ao amin'ny folder templates/")
        
        else:
            # Raha misy file hafa tadiavina
            super().do_GET()

# 3. Mandefa ny Server
with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Server mandeha ao amin'ny: http://localhost:{PORT}")
    print(f"Raha ao amin'ny Render ianao dia ampiasao ny Start Command: python app/server.py")
    httpd.serve_forever()

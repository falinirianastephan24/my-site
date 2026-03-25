import cherrypy
import os
import sqlite3

# 1. Mamorona ny Database
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS abc (id INTEGER PRIMARY KEY, texte TEXT)')
    hafatra_tongasoa = "Tongasoa avy amin'ny DB!"
    cursor.execute("INSERT INTO abc (texte) SELECT ? WHERE NOT EXISTS (SELECT 1 FROM abc)", (hafatra_tongasoa,))
    conn.commit()
    conn.close()

class WebServer(object):
    @cherrypy.expose
    def index(self):
        # 2. Maka data avy amin'ny DB
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT texte FROM abc LIMIT 1')
        resaka = cursor.fetchone() # Mamoaka tuple izy eto
        conn.close()

        # 3. Mitady ny lalana (path) mankany amin'ny HTML
        current_dir = os.path.dirname(os.path.abspath(__file__))
        html_path = os.path.join(current_dir, "dossier_html", "index.html")

        # 4. Mamaky ny HTML ary manolo ny {{hafatra}}
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
            # resaka[0] no ampiasaina mba tsy hisy fononteny ()
            return html_content.replace("{{hafatra}}", str(resaka[0]))

if __name__ == '__main__':
    init_db()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 1. Raiso ny Port omen'ny Render (default 10000 raha tsy misy)
    port = int(os.environ.get("PORT", 10000))
    
    # 2. Ampidiro ny config ho an'ny Server (Host 0.0.0.0 no ilain'ny Render)
    cherrypy.config.update({
        'server.socket_host': '0.0.0.0',
        'server.socket_port': port,
    })
    
    config = {
        '/css_sy_sary': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.join(current_dir, 'css_sy_sary')
        }
    }
    
    cherrypy.quickstart(WebServer(), '/', config)

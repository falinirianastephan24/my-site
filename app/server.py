from flask import Flask, render_template
import sqlite3, os

app = Flask(__name__, template_folder='../templates', static_folder='../static')
DB_PATH = os.path.join(os.path.dirname(__file__), 'database.db')

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS olona (anarana TEXT)")
        # Ampio ohatra raha mbola banga
        res = conn.execute("SELECT COUNT(*) FROM olona").fetchone()
        if res[0] == 0:
            conn.execute("INSERT INTO olona (anarana) VALUES ('Rakoto'), ('Rabe')")

@app.route('/')
def index():
    init_db()
    with sqlite3.connect(DB_PATH) as conn:
        olona = conn.execute("SELECT anarana FROM olona").fetchall()
    return render_template('index.html', olona=olona)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

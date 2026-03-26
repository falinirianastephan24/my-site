from flask import Flask, render_template, request, redirect
import sqlite3, os

app = Flask(__name__, template_folder='../templates', static_folder='../static')
UPLOAD_FOLDER = os.path.join(app.static_folder, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True) # Mamorona folder uploads raha tsy mbola misy
DB_PATH = os.path.join(os.path.dirname(__file__), 'database.db')

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS olona (anarana TEXT, sary TEXT)")

@app.route('/')
def index():
    init_db()
    with sqlite3.connect(DB_PATH) as conn:
        olona = conn.execute("SELECT anarana, sary FROM olona").fetchall()
    return render_template('index.html', olona=olona)

@app.route('/add', methods=['POST'])
def add():
    anarana = request.form.get('anarana')
    file = request.files.get('sary')
    
    if file:
        file.save(os.path.join(UPLOAD_FOLDER, file.filename)) # Tehirizina ao amin'ny static/uploads
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("INSERT INTO olona (anarana, sary) VALUES (?, ?)", (anarana, file.filename))
    return redirect('/')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

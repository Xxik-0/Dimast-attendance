from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# 데이터베이스 연결 및 테이블 생성 (최초 1회)
def init_db():
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, 'soccer_team.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS attendance 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, status TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, 'soccer_team.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # 참석 인원만 집계
    c.execute("SELECT name FROM attendance WHERE status='참석'")
    members = c.fetchall()
    conn.close()
    return render_template('index.html', members=members, count=len(members))

@app.route('/join', methods=['POST'])
def join():
    name = request.form['name']
    status = request.form['status']
    
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, 'soccer_team.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # 기존 데이터가 있으면 업데이트, 없으면 삽입
    c.execute("INSERT INTO attendance (name, status) VALUES (?, ?)", (name, status))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

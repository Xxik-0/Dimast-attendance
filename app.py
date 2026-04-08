import os
import sqlite3
from flask import Flask, render_template, request, redirect

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, template_folder=os.path.join(basedir, 'templates'))
db_path = os.path.join(basedir, 'soccer_team.db')

def init_db():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS attendance 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, status TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        
        # 각 상태별로 명단 가져오기
        c.execute("SELECT name FROM attendance WHERE status='참석'")
        attending = c.fetchall()
        
        c.execute("SELECT name FROM attendance WHERE status='미정'")
        undecided = c.fetchall()

        c.execute("SELECT name FROM attendance WHERE status='불참'")
        absent = c.fetchall()
        
        conn.close()
        
        return render_template('index.html', 
                               attending=attending, 
                               undecided=undecided, 
                               absent=absent,
                               attending_count=len(attending),
                               undecided_count=len(undecided),
                               absent_count=len(absent))
    except Exception as e:
        return f"데이터 로딩 중 에러: {e}"

@app.route('/join', methods=['POST'])
def join():
    name = request.form.get('name')
    status = request.form.get('status')
    
    if name:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("SELECT id FROM attendance WHERE name=?", (name,))
        existing = c.fetchone()
        
        if existing:
            c.execute("UPDATE attendance SET status=? WHERE name=?", (status, name))
        else:
            c.execute("INSERT INTO attendance (name, status) VALUES (?, ?)", (name, status))
            
        conn.commit()
        conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

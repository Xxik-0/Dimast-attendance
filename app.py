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
        
        # 1. 참석자 명단 가져오기
        c.execute("SELECT name FROM attendance WHERE status='참석'")
        attending = c.fetchall()
        
        # 2. 미정 명단 가져오기 (추가)
        c.execute("SELECT name FROM attendance WHERE status='미정'")
        undecided = c.fetchall()
        
        conn.close()
        
        return render_template('index.html', 
                               attending=attending, 
                               undecided=undecided, 
                               attending_count=len(attending),
                               undecided_count=len(undecided))
    except Exception as e:
        init_db()
        return f"데이터 로딩 중... 잠시 후 새로고침 해주세요. ({e})"

@app.route('/join', methods=['POST'])
def join():
    name = request.form.get('name')
    status = request.form.get('status')
    
    if name:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        # 이름이 이미 있는지 확인 (수정 기능)
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

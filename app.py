import os
import sqlite3
from flask import Flask, render_template, request, redirect

# [수정] 템플릿 경로를 명확하게 지정합니다.
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, template_folder=os.path.join(basedir, 'templates'))

db_path = os.path.join(basedir, 'soccer_team.db')

def init_db():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # 테이블이 없으면 생성
    c.execute('''CREATE TABLE IF NOT EXISTS attendance 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, status TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("SELECT name FROM attendance WHERE status='참석'")
        members = c.fetchall()
        conn.close()
        # 데이터가 하나도 없을 경우를 대비해 빈 리스트 전달
        return render_template('index.html', members=members, count=len(members))
    except Exception as e:
        # 에러 발생 시 화면에 에러 내용을 출력 (디버깅용)
        return f"DB 에러 발생: {e}"

@app.route('/join', methods=['POST'])
def join():
    name = request.form.get('name')
    status = request.form.get('status')
    
    if name:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("INSERT INTO attendance (name, status) VALUES (?, ?)", (name, status))
        conn.commit()
        conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()  # 서버 시작 전 반드시 DB 초기화
    app.run(debug=True)

import os
import sqlite3
from flask import Flask, render_template, request, redirect

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, template_folder=os.path.join(basedir, 'templates'))
db_path = os.path.join(basedir, 'soccer_team.db')

# [수정] 테이블 생성을 더 확실하게 보장하는 함수
def init_db():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # IF NOT EXISTS를 써서 테이블이 없을 때만 만듭니다.
    c.execute('''CREATE TABLE IF NOT EXISTS attendance 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, status TEXT)''')
    conn.commit()
    conn.close()

# [중요] 앱이 시작될 때 강제로 실행되도록 설정
init_db() 

@app.route('/')
def index():
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("SELECT name FROM attendance WHERE status='참석'")
        members = c.fetchall()
        conn.close()
        return render_template('index.html', members=members, count=len(members))
    except Exception as e:
        # 만약 또 에러가 나면 여기서 강제로 테이블을 한 번 더 만듭니다.
        init_db()
        return f"DB 초기화 중입니다. 새로고침(F5)을 눌러주세요. (에러내용: {e})"

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

# Render 환경(Gunicorn)에서는 아래 블록이 실행되지 않을 수 있으므로 
# 위에서 init_db()를 직접 호출하는 것이 안전합니다.
if __name__ == '__main__':
    app.run(debug=True)

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
    # 테이블이 없을 때만 생성합니다.
    c.execute('''CREATE TABLE IF NOT EXISTS attendance 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, status TEXT)''')
    conn.commit()
    conn.close()

# [중요] Flask 앱이 로드될 때 즉시 실행되도록 위치를 옮깁니다.
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
    except sqlite3.OperationalError:
        # 만약 테이블이 없다는 에러가 나면 여기서 한 번 더 생성 시도
        init_db()
        return "데이터베이스를 준비 중입니다. 잠시 후 새로고침(F5)을 눌러주세요."

@app.route('/join', methods=['POST'])
def join():
    @app.route('/join', methods=['POST'])
def join():
    name = request.form.get('name')
    status = request.form.get('status')
    
    if name:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        
        # 1. 먼저 이 이름이 명단에 있는지 확인합니다.
        c.execute("SELECT id FROM attendance WHERE name=?", (name,))
        existing_user = c.fetchone()
        
        if existing_user:
            # 2. 이미 있다면 상태(참석/불참)만 업데이트합니다.
            c.execute("UPDATE attendance SET status=? WHERE name=?", (status, name))
        else:
            # 3. 없다면 새로 추가합니다.
            c.execute("INSERT INTO attendance (name, status) VALUES (?, ?)", (name, status))
            
        conn.commit()
        conn.close()
    return redirect('/')
# Render(Gunicorn) 환경에서는 아래 블록이 무시될 수 있습니다.
if __name__ == '__main__':
    app.run(debug=True)

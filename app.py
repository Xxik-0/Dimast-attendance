import os
import sqlite3
from flask import Flask, render_template, request, redirect

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, template_folder=os.path.join(basedir, 'templates'))
db_path = os.path.join(basedir, 'soccer_team.db')

# [등록] 팀 전체 명단 (총 44명)
TOTAL_TEAM_LIST = [
    "강로빈", "강민재", "강인태", "김규민", "김대욱", "김명식", "김영서", "김정호", 
    "김주협", "김진일", "김창현", "김태완", "김호중", "류병수", "박종훈", "백민준", 
    "변시훈", "선우기단", "신민호", "양정현", "여민수", "오준택", "오현준", "이건기", 
    "이명주", "이은규", "이이유종", "이재동", "이재천", "이정열", "이찬주", "이태인", 
    "이하민", "임채윤", "전봉석", "정용환", "정호제", "진영훈", "최광수", "최연준", 
    "최주녕", "최현용", "한지성", "황영식"
]

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
        c.execute("SELECT name, status FROM attendance")
        voted_data = c.fetchall()
        conn.close()

        # 상태별 분류 (이름만 추출)
        attending = [name for name, status in voted_data if status == '참석']
        undecided = [name for name, status in voted_data if status == '미정']
        absent = [name for name, status in voted_data if status == '불참']
        
        # 미참여자 계산 (전체 명단 - 투표한 명단)
        voted_names = [name for name, status in voted_data]
        not_voted = [name for name in TOTAL_TEAM_LIST if name not in voted_names]

        return render_template('index.html', 
                               attending=attending, 
                               undecided=undecided, 
                               absent=absent,
                               not_voted=not_voted,
                               attending_count=len(attending),
                               undecided_count=len(undecided),
                               absent_count=len(absent),
                               not_voted_count=len(not_voted))
    except Exception as e:
        return f"에러 발생: {e}"

@app.route('/join', methods=['POST'])
def join():
    name = request.form.get('name', '').strip()
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

@app.route('/delete/<name>')
def delete(name):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("DELETE FROM attendance WHERE name=?", (name,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

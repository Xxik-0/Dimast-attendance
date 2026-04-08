import os
import sqlite3
from flask import Flask, render_template, request, redirect

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, template_folder=os.path.join(basedir, 'templates'))
db_path = os.path.join(basedir, 'soccer_team.db')

# [등록] 팀 전체 명단 (총 44명)
TOTAL_TEAM_LIST = [
    "황영식", "강민재", "최광수", "선우기단", "김규민", "김주협", "김진일", "김창현", 
    "김영서", "김태완", "김호중", "김대욱", "강로빈", "류병수", "이명주", "전봉석", 
    "변시훈", "신민호", "양정현", "여민수", "진영훈", "정용환", "이유종", "이건기", 
    "이은규", "이정열", "이태인", "이하민", "강인태", "임채윤", "이재동", "이재천", 
    "김정호", "정호제", "박종훈", "최주녕", "이찬주", "최연준", "한지성", "최현용", 
    "백민준", "오현준", "오준택", "김명식"
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

        # 상태별 분류
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
    name = request.form.get('name', '').strip() # 공백 제거
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

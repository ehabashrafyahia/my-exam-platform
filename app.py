from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# إعداد قاعدة البيانات
def init_db():
    conn = sqlite3.connect('results.db')
    c = conn.cursor()
    # إنشاء جدول لحفظ النتائج لو مش موجود
    c.execute('''CREATE TABLE IF NOT EXISTS students
                 (id INTEGER PRIMARY KEY, name TEXT, grade TEXT, score INTEGER)''')
    conn.commit()
    conn.close()

# تشغيل قاعدة البيانات عند بدء التطبيق
init_db()

# الأسئلة وإجاباتها الصحيحة (ممكن تزود براحتك)
QUESTIONS = [
    {'id': 1, 'text': 'ما هي عاصمة مصر؟', 'options': ['الإسكندرية', 'القاهرة', 'الجيزة'], 'answer': 'القاهرة'},
    {'id': 2, 'text': 'كم عدد ألوان علم مصر؟', 'options': ['2', '3', '4'], 'answer': '3'},
    {'id': 3, 'text': 'ناتج 5 * 5 يساوي؟', 'options': ['20', '25', '30'], 'answer': '25'}
]

# 1. الصفحة الرئيسية (دخول الطالب)
@app.route('/')
def home():
    return render_template('index.html')

# 2. صفحة الامتحان
@app.route('/quiz', methods=['POST'])
def quiz():
    name = request.form['name']
    grade = request.form['grade']
    return render_template('quiz.html', name=name, grade=grade, questions=QUESTIONS)

# 3. معالجة الإجابات وحساب النتيجة
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    grade = request.form['grade']
    score = 0
    
    # تصحيح الإجابات
    for q in QUESTIONS:
        user_answer = request.form.get(f'q_{q["id"]}')
        if user_answer == q['answer']:
            score += 1
    
    # حفظ النتيجة في قاعدة البيانات
    conn = sqlite3.connect('results.db')
    c = conn.cursor()
    c.execute("INSERT INTO students (name, grade, score) VALUES (?, ?, ?)", (name, grade, score))
    conn.commit()
    conn.close()
    
    return render_template('result.html', name=name, score=score, total=len(QUESTIONS))

# 4. لوحة تحكم المدرس (عرض النتائج)
@app.route('/admin')
def admin():
    conn = sqlite3.connect('results.db')
    c = conn.cursor()
    c.execute("SELECT * FROM students ORDER BY id DESC") # عرض أحدث النتائج أولاً
    data = c.fetchall()
    conn.close()
    return render_template('admin.html', students=data)

if __name__ == '__main__':
    app.run(debug=True)

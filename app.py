from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def init_db():
    conn = sqlite3.connect('staff.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS staff (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        role TEXT NOT NULL
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        staff_id INTEGER,
        date TEXT,
        time_in TEXT,
        time_out TEXT
    )''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    conn = sqlite3.connect('staff.db')
    c = conn.cursor()
    c.execute("SELECT * FROM staff")
    staff = c.fetchall()
    c.execute("SELECT s.name, a.date, a.time_in, a.time_out FROM attendance a JOIN staff s ON a.staff_id = s.id")
    records = c.fetchall()
    conn.close()
    return render_template('admin.html', staff=staff, records=records)

@app.route('/add_staff', methods=['POST'])
def add_staff():
    name = request.form['name']
    role = request.form['role']
    conn = sqlite3.connect('staff.db')
    c = conn.cursor()
    c.execute("INSERT INTO staff (name, role) VALUES (?, ?)", (name, role))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

@app.route('/clockin', methods=['POST'])
def clockin():
    staff_id = request.form['staff_id']
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time_in = now.strftime("%H:%M:%S")
    conn = sqlite3.connect('staff.db')
    c = conn.cursor()
    c.execute("INSERT INTO attendance (staff_id, date, time_in) VALUES (?, ?, ?)", (staff_id, date, time_in))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

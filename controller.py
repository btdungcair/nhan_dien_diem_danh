import time
import helper
import sqlite3
from sqlite3 import Error

def create_connection(db_file="test.db"):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

# Table user
def check_login(username, password):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM user WHERE username=? AND password=?", (username, password))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    if len(rows) == 1:
        return True
    else:
        return False

# Table students
def get_students_list():
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def get_id_list():
    student_list = get_students_list()
    id_list = [student[0] for student in student_list]
    return id_list

def get_sorted_students_list():
    return helper.sort_by_name(get_students_list())

def get_student(id):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students WHERE id=?", (id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def add_student(id, fullname, gender, dob, absent_count, image_path):
    conn = create_connection()
    cur = conn.cursor()
    image = helper.image_to_octet_string(image_path)
    cur.execute("INSERT INTO students (id, fullname, gender, dob, absent_count, image) VALUES (?, ?, ?, ?, ?, ?)", (id, fullname, gender, dob, absent_count, image))
    conn.commit()
    cur.close()
    conn.close()

def update_student(old_id, id, fullname, gender, dob, absent_count, image_data):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("UPDATE students SET id=?, fullname=?, gender=?, dob=?, absent_count=?, image=? WHERE id=?", (id, fullname, gender, dob, absent_count, image_data, old_id))
    conn.commit()
    cur.close()
    conn.close()

def update_absent_count_for_all_student():
    dates_count = len(get_dates_list())
    for student in get_students_list():
        attendance_count = get_attendance_count_by_id(student[0])
        absent_count = dates_count - attendance_count
        if absent_count < 0:
            absent_count = 0
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("UPDATE students SET absent_count=? WHERE id=?", (absent_count, student[0]))
        conn.commit()
        cur.close()
        conn.close()

def update_absent_count(id):
    dates_count = len(get_dates_list())
    attendance_count = get_attendance_count_by_id(id)
    absent_count = dates_count - attendance_count
    if absent_count < 0:
        absent_count = 0
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("UPDATE students SET absent_count=? WHERE id=?", (absent_count, id))
    conn.commit()
    cur.close()
    conn.close()

def delete_student(id):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    cur.close()
    conn.close()

# Table dates
def add_date(date=time.strftime("%d/%m/%Y")):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO dates (date) VALUES (?)", (date,))
    conn.commit()
    cur.close()
    conn.close()

def get_dates_list():
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM dates")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    dates = [date[0] for date in rows]
    return sorted(dates, key=lambda date: time.strptime(date, "%d/%m/%Y"))

def check_date(date):
    if date in get_dates_list():
        return True
    else:
        return False

# Table attendance
def attendance(student_id_set, date=time.strftime("%d/%m/%Y")):
    need_to_attendance = []
    for i in range(len(student_id_set)):
        if not check_exist_attendance_record(student_id_set[i], date):
            need_to_attendance.append(student_id_set[i])          
    if check_date(date) != True:
        add_date(date)
    conn = create_connection()
    cur = conn.cursor()
    for student_id in need_to_attendance:
        cur.execute("INSERT INTO attendance (student_id, date) VALUES (?, ?)", (student_id, date))
    conn.commit()
    cur.close()
    conn.close()
    update_absent_count_for_all_student()

def remove_attendance(student_id, date):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM attendance WHERE student_id=? AND date=?", (student_id, date))
    conn.commit()
    cur.close()
    conn.close()
    update_absent_count(student_id)

def attendance_late(student_id, date):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO attendance (student_id, date) VALUES (?, ?)", (student_id, date))
    conn.commit()
    cur.close()
    conn.close()
    update_absent_count(student_id)

def update_attendance(student_id, new_student_id):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("UPDATE attendance SET student_id=? WHERE student_id=?", (new_student_id, student_id))
    conn.commit()
    cur.close()
    conn.close()

def get_attendance_count_by_id(id):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM attendance WHERE student_id=?", (id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return len(rows)

def get_attendance(student_id):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT date FROM attendance WHERE student_id=?", (student_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    dates = [date[0] for date in rows]
    dates = sorted(dates, key=lambda date: time.strptime(date, "%d/%m/%Y"))
    res = []
    for date in get_dates_list():
        if date in dates:
            res.append("x")
        else:
            res.append("vắng")
    return res

def check_exist_attendance_record(student_id, date):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM attendance WHERE student_id=? AND date=?", (student_id, date))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    if len(rows) == 0:
        return False
    else:
        return True
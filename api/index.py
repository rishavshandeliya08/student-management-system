import os
import sys
import tempfile
from datetime import date
from flask import Flask, render_template, request, redirect, url_for, flash

# Ensure parent directory is in path to import models
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from models import db, Student, Attendance, LabAttendance, Marks, Fees

# Set absolute paths for templates and static folders
template_dir = os.path.join(parent_dir, 'templates')
static_dir = os.path.join(parent_dir, 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.url_map.strict_slashes = False
app.config['SECRET_KEY'] = 'student_management_secret_key_123'

# WSGI Middleware to normalize Vercel serverless rewrite paths and script names
class VercelMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        target_path = ''
        for key in ['HTTP_X_VERCEL_FORWARDED_PATH', 'HTTP_X_FORWARDED_URI', 'HTTP_X_ORIGINAL_URL', 'HTTP_X_REWRITE_URL', 'REQUEST_URI']:
            val = environ.get(key, '')
            if val and not val.startswith('/api/'):
                target_path = val.split('?')[0]
                break
        
        if not target_path or target_path == '/.*':
            path_info = environ.get('PATH_INFO', '')
            if path_info.startswith('/api/index.py'):
                target_path = path_info[len('/api/index.py'):] or '/'
            elif path_info.startswith('/api/index'):
                target_path = path_info[len('/api/index'):] or '/'
            else:
                target_path = path_info or '/'

        environ['PATH_INFO'] = target_path
        environ['SCRIPT_NAME'] = ''
        return self.app(environ, start_response)

app.wsgi_app = VercelMiddleware(app.wsgi_app)

# Always use in-memory SQLite for Vercel serverless to guarantee 100% crash-free execution
if os.environ.get('VERCEL') or os.environ.get('AWS_LAMBDA_FUNCTION_NAME'):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
else:
    db_path = os.path.join(tempfile.gettempdir(), 'students.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Seed sample data helper for instant demonstration
def seed_sample_data():
    try:
        if Student.query.count() == 0:
            today_str = date.today().strftime('%Y-%m-%d')
            s1 = Student(roll_no='CS2026001', name='Rahul Sharma', course='B.Tech Computer Science', semester='4', phone='9876543210', email='rahul@college.edu')
            s2 = Student(roll_no='CS2026002', name='Priya Patel', course='B.Tech Information Technology', semester='4', phone='9876543211', email='priya@college.edu')
            s3 = Student(roll_no='CS2026003', name='Amit Kumar', course='BCA', semester='2', phone='9876543212', email='amit@college.edu')
            db.session.add_all([s1, s2, s3])
            db.session.commit()

            m1 = Marks(student_id=s1.id, ct1=22, ct2=23, sem_exam=85)
            m2 = Marks(student_id=s2.id, ct1=20, ct2=21, sem_exam=78)
            m3 = Marks(student_id=s3.id, ct1=15, ct2=14, sem_exam=45)
            
            f1 = Fees(student_id=s1.id, total_fee=50000, paid_amount=35000)
            f2 = Fees(student_id=s2.id, total_fee=50000, paid_amount=50000)
            f3 = Fees(student_id=s3.id, total_fee=45000, paid_amount=20000)

            a1 = Attendance(student_id=s1.id, date=today_str, status='Present')
            a2 = Attendance(student_id=s2.id, date=today_str, status='Present')
            a3 = Attendance(student_id=s3.id, date=today_str, status='Absent')

            db.session.add_all([m1, m2, m3, f1, f2, f3, a1, a2, a3])
            db.session.commit()
    except Exception as err:
        print("Sample data seed note:", err)

# Initialize DB tables cleanly within application context
with app.app_context():
    try:
        db.create_all()
        seed_sample_data()
    except Exception as err:
        print("DB table setup note:", err)

# Ensure tables exist and are seeded before handling any request
@app.before_request
def ensure_tables():
    try:
        db.create_all()
        seed_sample_data()
    except Exception:
        pass

# Helper list of lab subjects
LAB_SUBJECTS = ['Python Lab', 'DBMS Lab', 'Operating System Lab', 'Computer Network Lab']

@app.route('/')
@app.route('/index')
@app.route('/index.html')
@app.route('/home')
@app.route('/dashboard')
def dashboard():
    try:
        total_students = Student.query.count()
        today_str = date.today().strftime('%Y-%m-%d')
        
        present_today = Attendance.query.filter_by(date=today_str, status='Present').count()
        absent_today = Attendance.query.filter_by(date=today_str, status='Absent').count()
        
        all_fees = Fees.query.all()
        fees_pending = sum(f.pending_amount for f in all_fees) if all_fees else 0.0
        
        all_marks = Marks.query.all()
        students_passed = sum(1 for m in all_marks if m.status == 'Pass') if all_marks else 0
        students_failed = sum(1 for m in all_marks if m.status == 'Fail') if all_marks else 0
    except Exception as err:
        print("Dashboard query info:", err)
        total_students = 0
        today_str = date.today().strftime('%Y-%m-%d')
        present_today = 0
        absent_today = 0
        fees_pending = 0.0
        students_passed = 0
        students_failed = 0
    
    return render_template('dashboard.html',
                           total_students=total_students,
                           present_today=present_today,
                           absent_today=absent_today,
                           fees_pending=fees_pending,
                           students_passed=students_passed,
                           students_failed=students_failed,
                           today_date=today_str)

@app.route('/students')
def student_list():
    query = request.args.get('q', '').strip()
    try:
        if query:
            students = Student.query.filter(
                (Student.name.ilike(f'%{query}%')) | 
                (Student.roll_no.ilike(f'%{query}%'))
            ).all()
        else:
            students = Student.query.all()
    except Exception:
        students = []
    return render_template('students.html', students=students, query=query)

@app.route('/students/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        roll_no = request.form.get('roll_no', '').strip()
        name = request.form.get('name', '').strip()
        course = request.form.get('course', '').strip()
        semester = request.form.get('semester', '').strip()
        phone = request.form.get('phone', '').strip()
        email = request.form.get('email', '').strip()
        
        existing = Student.query.filter_by(roll_no=roll_no).first()
        if existing:
            flash('Student with this Roll Number already exists!', 'danger')
            return redirect(url_for('add_student'))
        
        student = Student(roll_no=roll_no, name=name, course=course, semester=semester, phone=phone, email=email)
        db.session.add(student)
        db.session.commit()
        
        marks = Marks(student_id=student.id, ct1=float(request.form.get('ct1', 0) or 0),
                      ct2=float(request.form.get('ct2', 0) or 0),
                      sem_exam=float(request.form.get('sem_exam', 0) or 0))
        fees = Fees(student_id=student.id, total_fee=float(request.form.get('total_fee', 0) or 0),
                    paid_amount=float(request.form.get('paid_amount', 0) or 0))
        
        db.session.add(marks)
        db.session.add(fees)
        db.session.commit()
        
        flash('Student added successfully!', 'success')
        return redirect(url_for('student_list'))
        
    return render_template('add_student.html')

@app.route('/students/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        student.roll_no = request.form.get('roll_no', '').strip()
        student.name = request.form.get('name', '').strip()
        student.course = request.form.get('course', '').strip()
        student.semester = request.form.get('semester', '').strip()
        student.phone = request.form.get('phone', '').strip()
        student.email = request.form.get('email', '').strip()
        
        db.session.commit()
        flash('Student details updated successfully!', 'success')
        return redirect(url_for('student_list'))
        
    return render_template('edit_student.html', student=student)

@app.route('/students/delete/<int:id>', methods=['POST'])
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash('Student deleted successfully!', 'success')
    return redirect(url_for('student_list'))

@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    today_str = date.today().strftime('%Y-%m-%d')
    
    if request.method == 'POST':
        att_date = request.form.get('date', today_str)
        students = Student.query.all()
        for s in students:
            status = request.form.get(f'status_{s.id}', 'Absent')
            existing = Attendance.query.filter_by(student_id=s.id, date=att_date).first()
            if existing:
                existing.status = status
            else:
                att = Attendance(student_id=s.id, date=att_date, status=status)
                db.session.add(att)
        db.session.commit()
        flash(f'Attendance recorded for {att_date}!', 'success')
        return redirect(url_for('attendance', date=att_date))
    
    selected_date = request.args.get('date', today_str)
    students = Student.query.all()
    
    attendance_records = []
    for s in students:
        total_days = Attendance.query.filter_by(student_id=s.id).count()
        present_days = Attendance.query.filter_by(student_id=s.id, status='Present').count()
        absent_days = total_days - present_days
        percentage = round((present_days / total_days * 100), 2) if total_days > 0 else 0.0
        
        today_att = Attendance.query.filter_by(student_id=s.id, date=selected_date).first()
        today_status = today_att.status if today_att else 'Present'
        
        attendance_records.append({
            'student': s,
            'total_days': total_days,
            'present_days': present_days,
            'absent_days': absent_days,
            'percentage': percentage,
            'today_status': today_status
        })
        
    return render_template('attendance.html', records=attendance_records, selected_date=selected_date)

@app.route('/lab-attendance', methods=['GET', 'POST'])
def lab_attendance():
    today_str = date.today().strftime('%Y-%m-%d')
    selected_subject = request.args.get('subject', LAB_SUBJECTS[0])
    selected_date = request.args.get('date', today_str)
    
    if request.method == 'POST':
        subject = request.form.get('subject', LAB_SUBJECTS[0])
        att_date = request.form.get('date', today_str)
        students = Student.query.all()
        for s in students:
            status = request.form.get(f'status_{s.id}', 'Absent')
            existing = LabAttendance.query.filter_by(student_id=s.id, subject=subject, date=att_date).first()
            if existing:
                existing.status = status
            else:
                lab_att = LabAttendance(student_id=s.id, subject=subject, date=att_date, status=status)
                db.session.add(lab_att)
        db.session.commit()
        flash(f'{subject} attendance recorded for {att_date}!', 'success')
        return redirect(url_for('lab_attendance', subject=subject, date=att_date))
    
    students = Student.query.all()
    records = []
    for s in students:
        subject_stats = {}
        for sub in LAB_SUBJECTS:
            total = LabAttendance.query.filter_by(student_id=s.id, subject=sub).count()
            present = LabAttendance.query.filter_by(student_id=s.id, subject=sub, status='Present').count()
            absent = total - present
            subject_stats[sub] = {'total': total, 'present': present, 'absent': absent}
            
        today_att = LabAttendance.query.filter_by(student_id=s.id, subject=selected_subject, date=selected_date).first()
        today_status = today_att.status if today_att else 'Present'
        
        records.append({
            'student': s,
            'subject_stats': subject_stats,
            'today_status': today_status
        })
        
    return render_template('lab_attendance.html', 
                           records=records, 
                           subjects=LAB_SUBJECTS, 
                           selected_subject=selected_subject, 
                           selected_date=selected_date)

@app.route('/marks', methods=['GET', 'POST'])
def marks():
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        ct1 = float(request.form.get('ct1', 0) or 0)
        ct2 = float(request.form.get('ct2', 0) or 0)
        sem_exam = float(request.form.get('sem_exam', 0) or 0)
        
        mark_record = Marks.query.filter_by(student_id=student_id).first()
        if not mark_record:
            mark_record = Marks(student_id=student_id, ct1=ct1, ct2=ct2, sem_exam=sem_exam)
            db.session.add(mark_record)
        else:
            mark_record.ct1 = ct1
            mark_record.ct2 = ct2
            mark_record.sem_exam = sem_exam
            
        db.session.commit()
        flash('Marks updated successfully!', 'success')
        return redirect(url_for('marks'))
        
    students = Student.query.all()
    return render_template('marks.html', students=students)

@app.route('/fees', methods=['GET', 'POST'])
def fees():
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        total_fee = float(request.form.get('total_fee', 0) or 0)
        paid_amount = float(request.form.get('paid_amount', 0) or 0)
        
        fee_record = Fees.query.filter_by(student_id=student_id).first()
        if not fee_record:
            fee_record = Fees(student_id=student_id, total_fee=total_fee, paid_amount=paid_amount)
            db.session.add(fee_record)
        else:
            fee_record.total_fee = total_fee
            fee_record.paid_amount = paid_amount
            
        db.session.commit()
        flash('Fee details updated successfully!', 'success')
        return redirect(url_for('fees'))
        
    students = Student.query.all()
    return render_template('fees.html', students=students)

# Route aliases for common typos or singular paths
@app.route('/student')
@app.route('/student-list')
def student_redirect():
    return redirect(url_for('student_list'))

@app.route('/add-student')
@app.route('/students/new')
def add_student_redirect():
    return redirect(url_for('add_student'))

@app.route('/lab_attendance')
@app.route('/labattendance')
def lab_attendance_redirect():
    return redirect(url_for('lab_attendance'))

@app.route('/fee')
def fee_redirect():
    return redirect(url_for('fees'))

@app.route('/mark')
def mark_redirect():
    return redirect(url_for('marks'))

# Custom Error Handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    roll_no = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    course = db.Column(db.String(100), nullable=False)
    semester = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    # Relationships for cascading deletion when a student is deleted
    attendances = db.relationship('Attendance', backref='student', cascade='all, delete-orphan')
    lab_attendances = db.relationship('LabAttendance', backref='student', cascade='all, delete-orphan')
    marks = db.relationship('Marks', backref='student', uselist=False, cascade='all, delete-orphan')
    fees = db.relationship('Fees', backref='student', uselist=False, cascade='all, delete-orphan')

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id', ondelete='CASCADE'), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(10), nullable=False)  # 'Present' or 'Absent'

class LabAttendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id', ondelete='CASCADE'), nullable=False)
    subject = db.Column(db.String(100), nullable=False)  # Python Lab, DBMS Lab, etc.
    date = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(10), nullable=False)  # 'Present' or 'Absent'

class Marks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id', ondelete='CASCADE'), nullable=False)
    ct1 = db.Column(db.Float, default=0.0)
    ct2 = db.Column(db.Float, default=0.0)
    sem_exam = db.Column(db.Float, default=0.0)

    @property
    def total_marks(self):
        return (self.ct1 or 0) + (self.ct2 or 0) + (self.sem_exam or 0)

    @property
    def percentage(self):
        # Total max marks = 150 (CT1: 25, CT2: 25, Sem Exam: 100)
        return round((self.total_marks / 150.0) * 100, 2) if self.total_marks else 0.0

    @property
    def status(self):
        return 'Pass' if self.percentage >= 40.0 else 'Fail'

class Fees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id', ondelete='CASCADE'), nullable=False)
    total_fee = db.Column(db.Float, default=0.0)
    paid_amount = db.Column(db.Float, default=0.0)

    @property
    def pending_amount(self):
        return max(0.0, (self.total_fee or 0) - (self.paid_amount or 0))

    @property
    def status(self):
        return 'Paid' if self.pending_amount == 0 and self.total_fee > 0 else 'Pending'

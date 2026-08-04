# Student Management System (Python Flask)

A beginner-friendly, clean, and responsive **Student Management System** built with **Python Flask**, **SQLite**, **SQLAlchemy**, **Bootstrap 5**, and **Jinja2**. Designed for college mini-projects and easy serverless cloud deployment on Vercel.

---

## 🌐 Live Public Application URL

👉 **[https://student-management-system-rishab.vercel.app](https://student-management-system-rishab.vercel.app)**

---

## 🌟 Key Features

1. **Dashboard Overview**:
   - Total registered students count.
   - Today's Present & Absent count.
   - Total Pending Fees accumulator.
   - Pass vs Fail student count based on examination marks.

2. **Student Management (CRUD)**:
   - Add new students with Roll Number, Name, Course, Semester, Phone, and Email.
   - View complete student directory.
   - Search student records instantly by Name or Roll Number.
   - Edit student details.
   - Delete student records with automatic cascade deletion.

3. **Attendance System**:
   - **Daily Attendance**: Log daily Present/Absent status.
   - **Monthly / Working Day Stats**: Automatically calculates Total Working Days, Present Days, Absent Days, and Attendance Percentage.

4. **Laboratory Attendance**:
   - Subject-wise practical attendance tracking for:
     - Python Lab
     - DBMS Lab
     - Operating System Lab
     - Computer Network Lab
   - Displays Total Classes, Present, and Absent per subject.

5. **Academic Marks & Results**:
   - Records CT-1 (Max 25), CT-2 (Max 25), and Semester Exam (Max 100) scores.
   - Automatically computes Total Marks and Percentage.
   - Shows **Pass** (≥40%) or **Fail** (<40%) status badge.

6. **Fee Management**:
   - Records Total Fee and Paid Amount.
   - Automatically calculates Pending Fee and marks status as **Fully Paid** or **Pending**.

---

## 📁 Folder Structure

```
student-management/
│
├── api/                # Vercel serverless entrypoint
│   └── index.py        # Crash-proof Vercel Flask handler
├── app.py              # Main Flask entrypoint for local testing
├── models.py           # SQLAlchemy database models
├── requirements.txt    # Python dependencies
├── vercel.json         # Vercel route rewrites & serverless build config
├── README.md           # Documentation & deployment guide
├── .gitignore          # Version control exclusions
│
├── templates/          # Jinja2 HTML templates
│   ├── base.html       # Shared layout & Bootstrap navigation
│   ├── index.html      # Index entry point
│   ├── dashboard.html  # Dashboard cards & statistics
│   ├── students.html   # Student table & search
│   ├── add_student.html# New student creation form
│   ├── edit_student.html# Student detail editor
│   ├── attendance.html # Daily & overall attendance register
│   ├── lab_attendance.html # Practical lab attendance log
│   ├── marks.html      # Examination marks & grades
│   └── fees.html       # Tuition fee tracker
│
└── static/             # Static UI assets
    └── style.css       # Custom modern CSS styling
```

---

## 🚀 Local Setup & Running Instructions

1. **Clone or Download the Project**:
   Ensure Python 3.8+ is installed on your computer.

2. **Install Dependencies**:
   Open your terminal in the project folder and run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   python app.py
   ```

4. **Access the App**:
   Open your browser and navigate to `http://127.0.0.1:5000`

---

## ☁️ Deploying on Vercel

1. **Push to GitHub**:
   Push your project repository to GitHub.

2. **Import to Vercel**:
   - Go to [Vercel.com](https://vercel.com).
   - Click **Add New Site** -> **Import Git Repository**.
   - Set the project name to `student-management-system-rishab`.
   - Click **Deploy**.

Your live URL will be:
👉 **`https://student-management-system-rishab.vercel.app`**

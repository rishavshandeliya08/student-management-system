# Student Management System (Python Flask)

A beginner-friendly, clean, and responsive **Student Management System** built with **Python Flask**, **SQLite**, **SQLAlchemy**, **Bootstrap 5**, and **Jinja2**. Designed for college mini-projects and easy free deployment to cloud platforms like Render.com.

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
├── app.py              # Main Flask application & routes
├── models.py           # SQLAlchemy database models
├── requirements.txt    # Python dependencies
├── Procfile            # Deployment process file for Render/Heroku
├── runtime.txt         # Python runtime environment
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

## ☁️ Step-by-Step Free Public Cloud Deployment Guide

### Option 1: Deploy on Render.com (Recommended - Public URL)

1. **Push to GitHub**:
   - Create a new public repository on GitHub (e.g. `student-management-system`).
   - Push all project files to your GitHub repository:
     ```bash
     git init
     git add .
     git commit -m "Initial commit of Student Management System"
     git branch -M main
     git remote add origin https://github.com/YOUR_USERNAME/student-management-system.git
     git push -u origin main
     ```

2. **Create Web Service on Render**:
   - Sign up / Log in to [Render.com](https://render.com/).
   - Click **New +** -> **Web Service**.
   - Select **Build and deploy from a Git repository** and connect your GitHub account.
   - Choose your `student-management-system` repository.

3. **Configure Settings**:
   - **Name**: `student-management-portal` (or your preferred unique name)
   - **Region**: Choose the closest location to you
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: Select **Free** tier

4. **Deploy**:
   - Click **Create Web Service**.
   - Render will build and deploy your project automatically.
   - Once deployed, your project will be live with a public URL such as:
     `https://student-management-portal.onrender.com`

---

### Option 2: Deploy on PythonAnywhere

1. Sign up for a free account at [PythonAnywhere.com](https://www.pythonanywhere.com/).
2. Open a **Bash Console** and clone your project from GitHub.
3. Create a virtual environment and install requirements:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 myenv
   pip install -r requirements.txt
   ```
4. Go to the **Web** tab, create a new Web App selecting **Flask**, set the WSGI configuration file path pointing to `app.py`.
5. Reload the web app and open your assigned URL (`https://yourusername.pythonanywhere.com`).

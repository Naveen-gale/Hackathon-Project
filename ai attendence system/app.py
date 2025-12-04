import os
import base64
from datetime import datetime

from flask import Flask, flash, redirect, render_template, request, session, url_for, jsonify
from models.student_model import get_student, save_student
from firebase_admin import db
from utils.email_send import send_email_notification

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret123'
app.config["UPLOAD_FOLDER"] = os.path.join("static", "uploads", "students")

# ---------------------- HOME ----------------------
@app.route('/')
def home():
    return render_template('main.html')

# ---------------------- LOGIN ----------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form["name"].strip()
        roll = request.form["roll"].strip()

        student = get_student(roll)

        if student and student.get("name", "").lower() == name.lower():
            session["roll"] = roll
            session["name"] = student["name"]
            return redirect(url_for("student_page"))
        else:
            flash("❌ Invalid Name or Roll Number", "error")
            return redirect(url_for("login"))

    return render_template("login.html")


# ---------------------- STUDENT DASHBOARD ----------------------
@app.route("/student")
def student_page():
    if "roll" not in session:
        return redirect(url_for("login"))

    roll = session["roll"]
    name = session["name"]

    ref = db.reference("attendance").child(roll)
    attendance = ref.get()

    attended = len(attendance) if attendance else 0
    max_attendance = 75
    percent = round((attended / max_attendance) * 100, 2)

    status = "Eligible" if percent >= 75 else "Not Eligible"

    return render_template(
        "student.html",
        name=name,
        roll=roll,
        attended=attended,
        max_attendance=max_attendance,
        percentage=percent,
        status=status
    )


# ---------------------- CAMERA PAGE ----------------------
@app.route("/attendance")
def attendance():
    # if "roll" not in session:
    #     return redirect(url_for("login"))
    return render_template("attendance.html")


# ---------------------- REGISTER ----------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        college = request.form["college"]
        name = request.form["name"]
        gmail = request.form["gmail"]
        roll = request.form["roll"]
        photo = request.files["photo"]

        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

        photo_path = os.path.join(app.config["UPLOAD_FOLDER"], f"{roll}.jpg")
        photo.save(photo_path)

        save_student(college, name, roll, photo_path, gmail)
        send_email_notification(name, roll, college, gmail)

        flash("🎉 Registration Successful!", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


# ---------------------- VERIFY ATTENDANCE ----------------------
@app.route("/capture_image", methods=["POST"])
def capture_image():

    if "roll" not in session:
        return jsonify({"status": "error", "message": "Login first"}), 403

    roll = session["roll"]
    student = get_student(roll)

    stored_photo = student["photo"]
    stored_photo_url = "/" + stored_photo.replace("\\", "/")

    # push attendance
    now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    ref = db.reference("attendance").child(roll)
    ref.push({
        "name": student["name"],
        "roll": roll,
        "time": now,
        "status": "Present"
    })

    return jsonify({
        "status": "success",
        "message": "Attendance Marked ✔️",
        "name": student["name"],
        "roll": roll,
        "photo": stored_photo_url
    })


# ============================================================
#                         ADMIN PANEL
# ============================================================

ADMIN_USER = "admin"
ADMIN_PASS = "1234"


@app.route("/admin")
def admin_redirect():
    return redirect(url_for("admin_login"))


# ---------------------- ADMIN LOGIN ----------------------
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        if user == ADMIN_USER and pwd == ADMIN_PASS:
            session["admin"] = True
            return redirect(url_for("admin_dashboard"))
        else:
            flash("❌ Wrong Admin Credentials", "error")
            return redirect(url_for("admin_login"))

    return render_template("admin_login.html")


# ---------------------- ADMIN DASHBOARD ----------------------
@app.route("/admin/dashboard")
def admin_dashboard():
    if "admin" not in session:
        return redirect(url_for("admin_login"))

    students = db.reference("students").get()
    return render_template("admin_dashboard.html", students=students)


# ---------------------- ADMIN VIEW STUDENTS ----------------------
@app.route("/admin/students")
def admin_students():
    if "admin" not in session:
        return redirect(url_for("admin_login"))

    students = db.reference("students").get()
    return render_template("admin_students.html", students=students)


# ---------------------- ADMIN VIEW EACH ATTENDANCE ----------------------
@app.route("/admin/attendance/<roll>")
def admin_attendance(roll):
    if "admin" not in session:
        return redirect(url_for("admin_login"))

    attendance = db.reference("attendance").child(roll).get()
    student = get_student(roll)

    return render_template(
        "admin_attendance.html",
        attendance=attendance,
        student=student
    )


# ---------------------- ADMIN LOGOUT ----------------------
@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect(url_for("admin_login"))


# ---------------------- MAIN ----------------------
if __name__ == '__main__':
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)

import smtplib
from email.mime.text import MIMEText

def send_email_notification(name, roll, college, email):
    sender_email = "your gmail address"
    sender_password = "gmail app password"  # ✔️ YOUR APP PASSWORD (OK)

    subject = "Registration Successful - AI Attendance System"
    body = f"""
Hello {name},

You are successfully registered in Fatima College AI Attendance System.

College      : {college}
Student Name : {name}
Roll Number  : {roll}
Email        : {email}

Now you can login and mark attendance.

Regards,
Fatima College
"""

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, msg.as_string())
            print("Email sent to:", email)

    except Exception as e:
        print("Email Error:", e)

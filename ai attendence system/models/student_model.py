import os
import firebase_admin
from firebase_admin import credentials, db

# -------------------------------------------------------
# FIREBASE INITIALIZATION
# -------------------------------------------------------
cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'your-database-url'
})


# -------------------------------------------------------
# SAVE STUDENT DATA
# -------------------------------------------------------
def save_student(college, name, roll, photo_path, gmail=None):
    """
    Saves student details in Firebase.
    Stores ABSOLUTE image path so DeepFace can read it.
    """

    # Convert relative local path to ABSOLUTE path
    absolute_photo_path = os.path.abspath(photo_path)

    data = {
        "college": college,
        "name": name,
        "roll": roll,
        "photo": absolute_photo_path,  # ⭐ IMPORTANT: full path!
    }

    if gmail:
        data["gmail"] = gmail

    ref = db.reference("students")
    ref.child(roll).set(data)


# -------------------------------------------------------
# GET STUDENT DATA
# -------------------------------------------------------
def get_student(roll):
    """
    Fetches a student's entire record from Firebase using roll number.
    """
    ref = db.reference("students")
    return ref.child(roll).get()

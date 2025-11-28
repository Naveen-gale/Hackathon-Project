// Dummy simulated database data
const sampleStudentData = {
  name: "Ananya Sharma",
  roll: "21BC1023",
  overallAttendance: 87,
};

// Set current date
function setCurrentDate() {
  const dateElement = document.getElementById("current-date");
  if (!dateElement) return;

  const today = new Date();
  const options = { weekday: "long", day: "numeric", month: "short", year: "numeric" };
  dateElement.textContent = today.toLocaleDateString("en-IN", options);
}

// AI Alert logic
function getAlertMessage(student) {
  if (student.overallAttendance >= 90) {
    return "Excellent! Your attendance is above 90%. Keep it up 🎉";
  } else if (student.overallAttendance >= 75) {
    return "Good! Your attendance is safe (above 75%). Maintain this consistency.";
  } else {
    return "Warning: Your attendance is below 75%. You may not be eligible for exams.";
  }
}

// Fill data on screen
function updateDashboard(student) {
  document.getElementById("student-name").textContent = student.name;
  document.getElementById("student-roll").textContent = "Roll: " + student.roll;
  document.getElementById("overall-attendance").textContent = student.overallAttendance + "%";
  document.getElementById("alert-text").textContent = getAlertMessage(student);
}

// Initialize
document.addEventListener("DOMContentLoaded", () => {
  setCurrentDate();
  updateDashboard(sampleStudentData);
});

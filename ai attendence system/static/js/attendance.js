const video = document.getElementById("camera");
const canvas = document.getElementById("snapshot");
const captureBtn = document.getElementById("captureBtn");

// Start camera
navigator.mediaDevices.getUserMedia({ video: true }).then(stream => {
    video.srcObject = stream;
});

// Capture image and send to backend
captureBtn.addEventListener("click", () => {
    const context = canvas.getContext("2d");
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    const imageData = canvas.toDataURL("image/jpeg");

    fetch("/capture_image", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ img: imageData })
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message);
    });
});

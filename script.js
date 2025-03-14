async function convertFile() {
    const fileInput = document.getElementById("fileInput");
    const conversionType = document.getElementById("conversionType").value;

    if (!fileInput.files.length) {
        alert("Please select a file to convert.");
        return;
    }

    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append("file", file);
    formData.append("type", conversionType);

    try {
        const response = await fetch("http://localhost:8000/convert", {
            method: "POST",
            body: formData,
        });

        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const link = document.getElementById("downloadLink");
            link.href = url;
            link.style.display = "block";
            link.textContent = "Download Converted File";
        } else {
            alert("Conversion failed. Try again.");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("An error occurred.");
    }
}

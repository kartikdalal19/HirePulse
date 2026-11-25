// const analyzeJDButton = document.getElementById("analyzeJDButton");

// analyzeJDButton.addEventListener("click", () => {
//     const jobTitle = document.getElementById("jobTitle").value.trim();
//     const jobDescription = document.getElementById("jobDescription").value.trim();

//     if (!jobTitle) {
//         alert("Please enter a job title.");
//         return;
//     }

//     if (!jobDescription) {
//         alert("Please enter a job description.");
//         return;
//     }

//     alert("Job description validation successful. API integration will be added next.");
// });









const analyzeJDButton = document.getElementById("analyzeJDButton");

analyzeJDButton.addEventListener("click", analyzeJobDescription);

async function analyzeJobDescription() {
    const jobTitle = document.getElementById("jobTitle").value.trim();
    const companyName = document.getElementById("companyName").value.trim();
    const jobDescription = document.getElementById("jobDescription").value.trim();

    if (!jobTitle) {
        alert("Please enter a job title.");
        return;
    }

    if (!jobDescription) {
        alert("Please enter a job description.");
        return;
    }

    const combinedJD = `Job Title: ${jobTitle}
Company: ${companyName || "Not specified"}

${jobDescription}`;

    const formData = new FormData();
    formData.append("jd_text", combinedJD);
    formData.append("file", new Blob([]), "");

    try {
        analyzeJDButton.disabled = true;
        analyzeJDButton.innerHTML = `
            <i class="fa-solid fa-spinner fa-spin"></i>
            Analyzing...
        `;

        const response = await fetch("https://hirepulse-k366.onrender.com/api/jd/analyze", {
            method: "POST",
            body: formData
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(
                result.detail || result.message || "JD analysis failed."
            );
        }

        if (result.status !== "analyzed") {
            throw new Error("The JD could not be analyzed successfully.");
        }

        sessionStorage.setItem("hirepulse_jd", JSON.stringify(result));

        window.location.href = "upload-resumes.html";

    } catch (error) {
        console.error("JD Analysis Error:", error);

        alert(
            error.message ||
            "Unable to connect to the backend. Please check that the backend is running."
        );

    } finally {
        analyzeJDButton.disabled = false;
        analyzeJDButton.innerHTML = `
            Analyze Job Description
            <i class="fa-solid fa-arrow-right"></i>
        `;
    }
}


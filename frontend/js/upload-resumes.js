
// const resumeInput = document.getElementById("resumeInput");
// const dropZone = document.getElementById("dropZone");
// const browseFilesBtn = document.getElementById("browseFilesBtn");
// const fileListSection = document.getElementById("fileListSection");
// const fileList = document.getElementById("fileList");
// const fileCount = document.getElementById("fileCount");
// const clearFilesBtn = document.getElementById("clearFilesBtn");
// const startMatchingBtn = document.getElementById("startMatchingBtn");

// let selectedFiles = [];

// const MAX_FILE_SIZE = 5 * 1024 * 1024;
// const ALLOWED_EXTENSIONS = ["pdf", "docx"];

// browseFilesBtn.addEventListener("click", () => resumeInput.click());

// resumeInput.addEventListener("change", (event) => {
//     addFiles(event.target.files);
//     resumeInput.value = "";
// });

// dropZone.addEventListener("dragover", (event) => {
//     event.preventDefault();
//     dropZone.classList.add("drag-active");
// });

// dropZone.addEventListener("dragleave", (event) => {
//     if (!dropZone.contains(event.relatedTarget)) {
//         dropZone.classList.remove("drag-active");
//     }
// });

// dropZone.addEventListener("drop", (event) => {
//     event.preventDefault();
//     dropZone.classList.remove("drag-active");
//     addFiles(event.dataTransfer.files);
// });

// clearFilesBtn.addEventListener("click", () => {
//     selectedFiles = [];
//     renderFiles();
// });

// startMatchingBtn.addEventListener("click", () => {
//     if (selectedFiles.length === 0) {
//         alert("Please select at least one resume.");
//         return;
//     }

//     alert("Resume selection successful. Backend integration will be added next.");
// });

// function addFiles(files) {
//     const incomingFiles = Array.from(files);
//     let rejectedFiles = [];

//     incomingFiles.forEach((file) => {
//         const extension = file.name.split(".").pop().toLowerCase();

//         if (!ALLOWED_EXTENSIONS.includes(extension)) {
//             rejectedFiles.push(`${file.name}: Unsupported format`);
//             return;
//         }

//         if (file.size > MAX_FILE_SIZE) {
//             rejectedFiles.push(`${file.name}: Exceeds 5 MB`);
//             return;
//         }

//         const alreadyExists = selectedFiles.some(
//             existingFile =>
//                 existingFile.name === file.name &&
//                 existingFile.size === file.size
//         );

//         if (!alreadyExists) {
//             selectedFiles.push(file);
//         }
//     });

//     renderFiles();

//     if (rejectedFiles.length > 0) {
//         alert("Some files were rejected:\n\n" + rejectedFiles.join("\n"));
//     }
// }

// function renderFiles() {
//     fileList.innerHTML = "";

//     fileListSection.style.display =
//         selectedFiles.length > 0 ? "block" : "none";

//     fileCount.textContent = selectedFiles.length;
//     startMatchingBtn.disabled = selectedFiles.length === 0;

//     selectedFiles.forEach((file, index) => {
//         const extension = file.name.split(".").pop().toLowerCase();
//         const fileType = extension === "pdf" ? "pdf" : "docx";
//         const icon = extension === "pdf"
//             ? "fa-file-pdf"
//             : "fa-file-word";

//         const fileItem = document.createElement("div");
//         fileItem.className = "file-item";

//         fileItem.innerHTML = `
//             <div class="file-icon ${fileType}">
//                 <i class="fa-solid ${icon}"></i>
//             </div>

//             <div class="file-info">
//                 <div class="file-name"></div>
//                 <div class="file-size">${formatFileSize(file.size)}</div>
//                 <div class="file-valid">
//                     <i class="fa-solid fa-circle-check"></i>
//                     Ready for analysis
//                 </div>
//             </div>

//             <button class="remove-file-btn" title="Remove file">
//                 <i class="fa-solid fa-trash"></i>
//             </button>
//         `;

//         fileItem.querySelector(".file-name").textContent = file.name;

//         fileItem.querySelector(".remove-file-btn").addEventListener(
//             "click",
//             () => {
//                 selectedFiles.splice(index, 1);
//                 renderFiles();
//             }
//         );

//         fileList.appendChild(fileItem);
//     });
// }

// function formatFileSize(bytes) {
//     if (bytes < 1024) return `${bytes} B`;
//     if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
//     return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
// }





const resumeInput = document.getElementById("resumeInput");
const dropZone = document.getElementById("dropZone");
const browseFilesBtn = document.getElementById("browseFilesBtn");
const fileListSection = document.getElementById("fileListSection");
const fileList = document.getElementById("fileList");
const fileCount = document.getElementById("fileCount");
const clearFilesBtn = document.getElementById("clearFilesBtn");
const startMatchingBtn = document.getElementById("startMatchingBtn");
let evaluatedCandidates = [];
let selectedFiles = [];

const MAX_FILE_SIZE = 5 * 1024 * 1024;
const ALLOWED_EXTENSIONS = ["pdf", "docx"];
const API_BASE_URL = "https://hirepulse-k366.onrender.com";

// ---------- File Selection ----------

browseFilesBtn.addEventListener("click", () => resumeInput.click());

resumeInput.addEventListener("change", (event) => {
    addFiles(event.target.files);
    resumeInput.value = "";
});

dropZone.addEventListener("dragover", (event) => {
    event.preventDefault();
    dropZone.classList.add("drag-active");
});

dropZone.addEventListener("dragleave", (event) => {
    if (!dropZone.contains(event.relatedTarget)) {
        dropZone.classList.remove("drag-active");
    }
});

dropZone.addEventListener("drop", (event) => {
    event.preventDefault();
    dropZone.classList.remove("drag-active");
    addFiles(event.dataTransfer.files);
});

clearFilesBtn.addEventListener("click", () => {
    selectedFiles = [];
    renderFiles();
});

startMatchingBtn.addEventListener("click", startMatching);

// ---------- Add Files ----------

function addFiles(files) {
    const incomingFiles = Array.from(files);
    let rejectedFiles = [];

    incomingFiles.forEach((file) => {
        const extension = file.name.split(".").pop().toLowerCase();

        if (!ALLOWED_EXTENSIONS.includes(extension)) {
            rejectedFiles.push(`${file.name}: Unsupported format`);
            return;
        }

        if (file.size > MAX_FILE_SIZE) {
            rejectedFiles.push(`${file.name}: Exceeds 5 MB`);
            return;
        }

        const alreadyExists = selectedFiles.some(
            existingFile =>
                existingFile.name === file.name &&
                existingFile.size === file.size
        );

        if (!alreadyExists) {
            selectedFiles.push(file);
        }
    });

    renderFiles();

    if (rejectedFiles.length > 0) {
        alert("Some files were rejected:\n\n" + rejectedFiles.join("\n"));
    }
}

// ---------- Render File List ----------

function renderFiles() {
    fileList.innerHTML = "";

    fileListSection.style.display =
        selectedFiles.length > 0 ? "block" : "none";

    fileCount.textContent = selectedFiles.length;
    startMatchingBtn.disabled = selectedFiles.length === 0;

    selectedFiles.forEach((file, index) => {
        const extension = file.name.split(".").pop().toLowerCase();
        const fileType = extension === "pdf" ? "pdf" : "docx";
        const icon = extension === "pdf"
            ? "fa-file-pdf"
            : "fa-file-word";

        const fileItem = document.createElement("div");
        fileItem.className = "file-item";

        fileItem.innerHTML = `
            <div class="file-icon ${fileType}">
                <i class="fa-solid ${icon}"></i>
            </div>

            <div class="file-info">
                <div class="file-name"></div>
                <div class="file-size">${formatFileSize(file.size)}</div>
                <div class="file-valid">
                    <i class="fa-solid fa-circle-check"></i>
                    Ready for analysis
                </div>
            </div>

            <button class="remove-file-btn" title="Remove file">
                <i class="fa-solid fa-trash"></i>
            </button>
        `;

        fileItem.querySelector(".file-name").textContent = file.name;

        fileItem.querySelector(".remove-file-btn").addEventListener(
            "click",
            () => {
                selectedFiles.splice(index, 1);
                renderFiles();
            }
        );

        fileList.appendChild(fileItem);
    });
}

// ---------- File Size ----------

function formatFileSize(bytes) {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
}

// ---------- Progress UI ----------

function createProgressUI() {
    let progressSection = document.getElementById("matchingProgressSection");

    if (!progressSection) {
        progressSection = document.createElement("div");
        progressSection.id = "matchingProgressSection";
        progressSection.className = "panel";
        progressSection.style.marginTop = "24px";

        progressSection.innerHTML = `
            <div class="panel-header">
                <div>
                    <h3>Matching Progress</h3>
                    <p id="matchingStatusText">Preparing evaluation...</p>
                </div>
            </div>

            <div style="background:rgba(255,255,255,0.08);
                        height:8px;border-radius:8px;overflow:hidden;
                        margin:16px 0;">
                <div id="matchingProgressBar"
                     style="height:100%;width:0%;
                     background:#8b5cf6;transition:width 0.3s;">
                </div>
            </div>

            <div id="candidateProgressList"></div>
        `;

        document.querySelector(".upload-panel").appendChild(progressSection);
    }

    return progressSection;
}

// ---------- Start Matching ----------

async function startMatching() {
    if (selectedFiles.length === 0) {
        alert("Please select at least one resume.");
        return;
    }

    const storedJD = sessionStorage.getItem("hirepulse_jd");

    if (!storedJD) {
        alert("Job description data not found. Please analyze the JD again.");
        return;
    }

    let jdRecord;

    try {
        jdRecord = JSON.parse(storedJD);
    } catch {
        alert("Stored job description data is invalid.");
        return;
    }

    const extractedJD = jdRecord.extracted_requirements;

    if (!extractedJD) {
        alert("Structured job requirements were not found.");
        return;
    }

    const formData = new FormData();

    formData.append("jd_data", JSON.stringify(extractedJD));

    selectedFiles.forEach((file) => {
        formData.append("files", file);
    });

    startMatchingBtn.disabled = true;
    clearFilesBtn.disabled = true;

    startMatchingBtn.innerHTML = `
        <i class="fa-solid fa-spinner fa-spin"></i>
        Evaluating...
    `;

    createProgressUI();

    const statusText = document.getElementById("matchingStatusText");
    const progressBar = document.getElementById("matchingProgressBar");
    const candidateProgressList = document.getElementById("candidateProgressList");

    candidateProgressList.innerHTML = "";

    try {
        const response = await fetch(`${API_BASE_URL}/api/batch/evaluate`, {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(errorText || "Batch evaluation request failed.");
        }

        if (!response.body) {
            throw new Error("Streaming response is not supported by this browser.");
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        let buffer = "";
        let completedCount = 0;
        const totalCandidates = selectedFiles.length;

        while (true) {
            const { value, done } = await reader.read();

            if (done) break;

            buffer += decoder.decode(value, { stream: true });

            const messages = buffer.split("\n\n");
            buffer = messages.pop() || "";

            for (const message of messages) {
                const dataLine = message
                    .split("\n")
                    .find(line => line.startsWith("data:"));

                if (!dataLine) continue;

                const jsonText = dataLine.slice(5).trim();

                if (!jsonText) continue;

                const eventData = JSON.parse(jsonText);

                // Candidate started
                if (eventData.event === "candidate_started") {
                    statusText.textContent =
                        `Evaluating ${eventData.candidate_number} of ${eventData.total_candidates}: ${eventData.filename}`;

                    addCandidateProgress(
                        eventData.candidate_id,
                        eventData.filename,
                        "Evaluating...",
                        "processing"
                    );
                }

                // Candidate completed
                // else if (eventData.event === "candidate_completed") {
                //     completedCount++;

                //     const candidate = eventData.candidate;
                //     console.log("Candidate evaluation payload:", candidate);
                //     console.log("Overall score:", candidate.overall_score);
                    
                //     updateCandidateProgress(
                //         candidate.candidate_id,
                //         `Completed - ${Number(candidate.overall_score).toFixed(2)}%`,
                //         "completed"
                //     );

                //     progressBar.style.width =
                //         `${(completedCount / totalCandidates) * 100}%`;

                //     statusText.textContent =
                //         `${completedCount} of ${totalCandidates} candidates processed`;
                // }

                // Candidate completed
                else if (eventData.event === "candidate_completed") {
                    completedCount++;

                    const candidate = eventData.candidate;

                    console.log("Candidate evaluation payload:", candidate);
                    console.log("Overall score:", candidate.overall_score);

                    // Add the newly evaluated candidate
                    evaluatedCandidates.push(candidate);

                    // Sort candidates by score (highest first)
                    evaluatedCandidates.sort(
                        (a, b) => b.overall_score - a.overall_score
                    );

                    // Reassign ranks dynamically
                    evaluatedCandidates.forEach((c, index) => {
                        c.rank = index + 1;
                    });

                    // Update the ranking table immediately
                    renderRanking(evaluatedCandidates);

                    updateCandidateProgress(
                        candidate.candidate_id,
                        `Completed - ${Number(candidate.overall_score).toFixed(2)}%`,
                        "completed"
                    );

                    progressBar.style.width =
                        `${(completedCount / totalCandidates) * 100}%`;

                    statusText.textContent =
                        `${completedCount} of ${totalCandidates} candidates processed`;
                }


                // Candidate failed
                else if (eventData.event === "candidate_failed") {
                    completedCount++;

                    const candidate = eventData.candidate;

                    updateCandidateProgress(
                        candidate.candidate_id,
                        `Failed: ${candidate.error || "Evaluation error"}`,
                        "failed"
                    );

                    progressBar.style.width =
                        `${(completedCount / totalCandidates) * 100}%`;

                    statusText.textContent =
                        `${completedCount} of ${totalCandidates} candidates processed`;
                }

                // Batch completed
                else if (eventData.event === "batch_completed") {
                    const result = eventData.result;
                    console.log("Final batch result:", result);
                    console.log("Ranked candidates:", result.ranked_candidates);
                    evaluatedCandidates = result.ranked_candidates || [];

                    statusText.textContent =
                        `Evaluation finished: ${result.successful_evaluations} successful, ${result.failed_evaluations} failed`;

                    progressBar.style.width = "100%";

                    renderRanking(result.ranked_candidates);
                    renderFailedCandidates(result.failed_candidates);
                }
            }
        }

    } catch (error) {
        console.error("Batch Evaluation Error:", error);

        statusText.textContent = "Evaluation failed.";

        const errorMessage = document.createElement("p");
        errorMessage.style.color = "#f87171";
        errorMessage.textContent = error.message;

        candidateProgressList.appendChild(errorMessage);

    } finally {
        startMatchingBtn.disabled = selectedFiles.length === 0;
        clearFilesBtn.disabled = false;

        startMatchingBtn.innerHTML = `
            Start Matching
            <i class="fa-solid fa-arrow-right"></i>
        `;
    }
}

// ---------- Candidate Progress ----------

function addCandidateProgress(candidateId, filename, status, className) {
    const list = document.getElementById("candidateProgressList");

    const item = document.createElement("div");
    item.id = `progress-${candidateId}`;
    item.style.cssText =
        "display:flex;justify-content:space-between;align-items:center;" +
        "gap:16px;padding:12px 0;border-bottom:1px solid rgba(255,255,255,0.08);";

    const filenameElement = document.createElement("span");
    filenameElement.textContent = filename;
    filenameElement.style.cssText = "overflow-wrap:anywhere;";

    const statusElement = document.createElement("span");
    statusElement.className = `candidate-status ${className}`;
    statusElement.textContent = status;

    item.appendChild(filenameElement);
    item.appendChild(statusElement);

    list.appendChild(item);
}

function updateCandidateProgress(candidateId, status, className) {
    const item = document.getElementById(`progress-${candidateId}`);

    if (!item) return;

    const statusElement = item.querySelector(".candidate-status");

    statusElement.textContent = status;
    statusElement.className = `candidate-status ${className}`;
}

// ---------- Final Ranking ----------

// function renderRanking(candidates) {
//     const section = document.getElementById("matchingProgressSection");

//     if (!candidates || candidates.length === 0) {
//         const emptyMessage = document.createElement("p");
//         emptyMessage.textContent = "No candidates were successfully evaluated.";
//         section.appendChild(emptyMessage);
//         return;
//     }

//     const rankingContainer = document.createElement("div");
//     rankingContainer.style.marginTop = "24px";

//     rankingContainer.innerHTML = `
//         <h3 style="margin-bottom:16px;">Candidate Ranking</h3>
//         <div id="rankingList"></div>
//     `;

//     section.appendChild(rankingContainer);

//     const rankingList = rankingContainer.querySelector("#rankingList");

//     candidates.forEach((candidate) => {
//         const card = document.createElement("div");

//         card.style.cssText =
//             "padding:16px;margin-bottom:12px;border:1px solid rgba(255,255,255,0.1);" +
//             "border-radius:12px;background:rgba(255,255,255,0.025);";

//         const name =
//             candidate.profile?.candidate_name ||
//             candidate.filename ||
//             "Unknown Candidate";

//         card.innerHTML = `
//             <div style="display:flex;justify-content:space-between;" +
//                      "align-items:center;gap:16px;flex-wrap:wrap;">
//                 <div>
//                     <h4 class="ranking-name"></h4>
//                     <small class="ranking-filename"></small>
//                 </div>

//                 <div style="text-align:right;">
//                     <div class="ranking-score"
//                          style="font-size:22px;font-weight:700;"></div>
//                     <small class="ranking-position"></small>
//                 </div>
//             </div>
//         `;

//         card.querySelector(".ranking-name").textContent = name;
//         card.querySelector(".ranking-filename").textContent =
//             candidate.filename || "";

//         card.querySelector(".ranking-score").textContent =
//             `${Number(candidate.overall_score).toFixed(2)}%`;

//         card.querySelector(".ranking-position").textContent =
//             `Rank #${candidate.rank}`;

//         rankingList.appendChild(card);
//     });
// }








// function renderRanking(candidates) {
//     const container = document.getElementById("candidateRanking");

//     if (!container) {
//         console.error("Candidate ranking container not found.");
//         return;
//     }

//     if (!candidates || candidates.length === 0) {
//         container.innerHTML = "<p>No candidates to display.</p>";
//         return;
//     }

//     const getRequiredSkills = (candidate) => {
//         const components = candidate.scoring?.components || {};
//         const skills = components.required_skills;

//         return skills?.matched_skills || skills?.matched || [];
//     };

//     container.innerHTML = `
//         <div class="ranking-table-wrapper">
//             <table class="ranking-table">
//                 <thead>
//                     <tr>
//                         <th>Rank</th>
//                         <th>Candidate</th>
//                         <th>Experience</th>
//                         <th>Match %</th>
//                         <th>Matched Skills</th>
//                         <th>Action</th>
//                     </tr>
//                 </thead>
//                 <tbody>
//                     ${candidates.map((candidate, index) => {
//                         const profile = candidate.profile || {};
//                         const score = Number(candidate.overall_score || 0);

//                         const experience =
//                             candidate.scoring?.components?.relevant_experience
//                                 ?.relevant_months;

//                         const experienceText =
//                             experience != null
//                                 ? `${(experience / 12).toFixed(1)} years`
//                                 : "N/A";

//                         const matchedSkills = getRequiredSkills(candidate);

//                         const skillsText = Array.isArray(matchedSkills)
//                             ? matchedSkills.map(skill =>
//                                 typeof skill === "string"
//                                     ? skill
//                                     : skill.skill || skill.name || ""
//                               ).filter(Boolean).join(", ")
//                             : "N/A";

//                         return `
//                             <tr>
//                                 <td>#${candidate.rank || index + 1}</td>
//                                 <td>
//                                     <div class="candidate-name">
//                                         ${profile.candidate_name || candidate.filename}
//                                     </div>
//                                     <small>${candidate.filename}</small>
//                                 </td>
//                                 <td>${experienceText}</td>
//                                 <td>
//                                     <span class="match-score">
//                                         ${score.toFixed(2)}%
//                                     </span>
//                                 </td>
//                                 <td>${skillsText || "N/A"}</td>
//                                 <td>
//                                     <button class="view-candidate-btn"
//                                         data-candidate-id="${candidate.candidate_id}">
//                                         View Analysis
//                                     </button>
//                                 </td>
//                             </tr>
//                         `;
//                     }).join("")}
//                 </tbody>
//             </table>
//         </div>
//     `;
// }













// function renderRanking(candidates) {
//     const section = document.getElementById("matchingProgressSection");

//     if (!section) return;

//     let container = document.getElementById("candidateRanking");

//     if (!container) {
//         container = document.createElement("div");
//         container.id = "candidateRanking";
//         container.style.marginTop = "28px";
//         section.appendChild(container);
//     }

//     if (!candidates || candidates.length === 0) {
//         container.innerHTML = "<p>No candidates were evaluated.</p>";
//         return;
//     }

//     function escapeHTML(value) {
//         return String(value ?? "").replace(/[&<>"']/g, char => ({
//             "&": "&amp;",
//             "<": "&lt;",
//             ">": "&gt;",
//             '"': "&quot;",
//             "'": "&#39;"
//         }[char]));
//     }

//     container.innerHTML = `
//         <h3 style="margin-bottom:16px;">Candidate Ranking</h3>

//         <div style="overflow-x:auto;">
//             <table class="ranking-table">
//                 <thead>
//                     <tr>
//                         <th>Rank</th>
//                         <th>Candidate</th>
//                         <th>Experience Match</th>
//                         <th>Match %</th>
//                         <th>Matched Skills</th>
//                         <th>Action</th>
//                     </tr>
//                 </thead>

//                 <tbody>
//                     ${candidates.map((candidate, index) => {
//                         const profile = candidate.candidate_profile || {};

//                         const components =
//                             candidate.component_breakdown || [];

//                         const requiredSkillsComponent =
//                             components.find(
//                                 c => c.component === "required_skills"
//                             );

//                         const experienceComponent =
//                             components.find(
//                                 c => c.component === "relevant_experience"
//                             );

//                         const matchedSkills =
//                             requiredSkillsComponent?.matched_evidence || [];

//                         const skillsText = matchedSkills
//                             .filter(skill => skill.found !== false)
//                             .map(skill => skill.skill)
//                             .filter(Boolean)
//                             .join(", ");

//                         const experienceText =
//                             experienceComponent
//                                 ? `${Number(experienceComponent.score || 0).toFixed(0)}% relevance`
//                                 : "Not evaluated";

//                         const candidateName =
//                             profile.candidate_name ||
//                             candidate.filename ||
//                             "Unknown Candidate";

//                         return `
//                             <tr>
//                                 <td>#${candidate.rank || index + 1}</td>

//                                 <td>
//                                     <strong>
//                                         ${escapeHTML(candidateName)}
//                                     </strong>
//                                     <br>
//                                     <small>
//                                         ${escapeHTML(candidate.filename)}
//                                     </small>
//                                 </td>

//                                 <td>${experienceText}</td>

//                                 <td>
//                                     <span class="match-score">
//                                         ${Number(candidate.overall_score || 0).toFixed(2)}%
//                                     </span>
//                                 </td>

//                                 <td>
//                                     ${escapeHTML(skillsText || "N/A")}
//                                 </td>

//                                 <td>
//                                     <button
//                                         class="view-candidate-btn"
//                                         data-candidate-id="${escapeHTML(candidate.candidate_id)}">
//                                         View Analysis
//                                     </button>
//                                 </td>
//                             </tr>
//                         `;
//                     }).join("")}
//                 </tbody>
//             </table>
//         </div>
//     `;
// }


function renderRanking(candidates) {
    const section = document.getElementById("matchingProgressSection");

    if (!section) return;

    let container = document.getElementById("candidateRanking");

    if (!container) {
        container = document.createElement("div");
        container.id = "candidateRanking";
        container.style.marginTop = "28px";
        section.appendChild(container);
    }

    if (!candidates || candidates.length === 0) {
        container.innerHTML = "<p>No candidates were evaluated.</p>";
        return;
    }

    function escapeHTML(value) {
        return String(value ?? "").replace(/[&<>"']/g, char => ({
            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
            '"': "&quot;",
            "'": "&#39;"
        }[char]));
    }

    container.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:center; gap:15px; flex-wrap:wrap; margin-bottom:16px;">
            <h3 style="margin:0;">Candidate Ranking</h3>

            <button id="downloadReportBtn" class="primary-button">
                <i class="fa-solid fa-file-pdf"></i>
                Download Detailed Report
            </button>
        </div>

        <div style="overflow-x:auto;">
            <table class="ranking-table">
                <thead>
                    <tr>
                        <th>Rank</th>
                        <th>Candidate</th>
                        <th>Experience Match</th>
                        <th>Match %</th>
                        <th>Matched Skills</th>
                        <th>Action</th>
                    </tr>
                </thead>

                <tbody>
                    ${candidates.map((candidate, index) => {
                        const profile = candidate.candidate_profile || {};

                        const components =
                            candidate.component_breakdown || [];

                        const requiredSkillsComponent =
                            components.find(
                                c => c.component === "required_skills"
                            );

                        const experienceComponent =
                            components.find(
                                c => c.component === "relevant_experience"
                            );

                        const matchedSkills =
                            requiredSkillsComponent?.matched_evidence || [];

                        const skillsText = matchedSkills
                            .filter(skill => skill.found !== false)
                            .map(skill => skill.skill)
                            .filter(Boolean)
                            .join(", ");

                        const experienceText =
                            experienceComponent
                                ? `${Number(experienceComponent.score || 0).toFixed(0)}% relevance`
                                : "Not evaluated";

                        const candidateName =
                            profile.candidate_name ||
                            candidate.filename ||
                            "Unknown Candidate";

                        return `
                            <tr>
                                <td>#${candidate.rank || index + 1}</td>

                                <td>
                                    <strong>
                                        ${escapeHTML(candidateName)}
                                    </strong>
                                    <br>
                                    <small>
                                        ${escapeHTML(candidate.filename)}
                                    </small>
                                </td>

                                <td>${experienceText}</td>

                                <td>
                                    <span class="match-score">
                                        ${Number(candidate.overall_score || 0).toFixed(2)}%
                                    </span>
                                </td>

                                <td>
                                    ${escapeHTML(skillsText || "N/A")}
                                </td>

                                <td>
                                    <button
                                        class="view-candidate-btn"
                                        data-candidate-id="${escapeHTML(candidate.candidate_id)}">
                                        View Analysis
                                    </button>
                                </td>
                            </tr>
                        `;
                    }).join("")}
                </tbody>
            </table>
        </div>
    `;
}


// ---------- Failed Candidates ----------

function renderFailedCandidates(failedCandidates) {
    if (!failedCandidates || failedCandidates.length === 0) return;

    const section = document.getElementById("matchingProgressSection");

    const failedContainer = document.createElement("div");
    failedContainer.style.marginTop = "24px";

    failedContainer.innerHTML = `
        <h3 style="margin-bottom:12px;">Failed Evaluations</h3>
    `;

    failedCandidates.forEach((candidate) => {
        const item = document.createElement("div");

        item.style.cssText =
            "padding:12px;margin-bottom:8px;border-radius:8px;" +
            "background:rgba(248,113,113,0.08);";

        item.textContent =
            `${candidate.filename}: ${candidate.error || "Evaluation failed"}`;

        failedContainer.appendChild(item);
    });

    section.appendChild(failedContainer);
}




function renderCandidateProfile(candidate) {

    const profile = candidate.candidate_profile || {};

    function escapeHTML(value) {
        return String(value ?? "").replace(/[&<>"']/g, char => ({
            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
            '"': "&quot;",
            "'": "&#39;"
        }[char]));
    }

    const education = profile.education || [];

    const educationHTML = education.length
        ? education.map(item => `
            <div class="profile-education-item">
                <strong>${escapeHTML(item.degree || "Degree")}</strong>
                <p>${escapeHTML(item.field || "")}</p>
                <p>${escapeHTML(item.institution || "Institution not specified")}</p>
                <p>${escapeHTML(item.graduation_year || "Year not specified")}</p>
            </div>
        `).join("")
        : "<p>Education details not available.</p>";

    const content = document.getElementById("candidateAnalysisContent");

    content.innerHTML = `
        <div class="candidate-profile-section">

            <div class="candidate-profile-top">
                <div class="candidate-avatar">
                    <i class="fas fa-user"></i>
                </div>

                <div>
                    <h2>${escapeHTML(profile.candidate_name || "Unknown Candidate")}</h2>
                    <p class="candidate-professional-title">
                        ${escapeHTML(profile.professional_title || "Professional title not available")}
                    </p>
                </div>
            </div>

            <div class="candidate-contact-grid">

                <div class="candidate-contact-item">
                    <i class="fas fa-envelope"></i>
                    <span>${escapeHTML(profile.email || "Email not available")}</span>
                </div>

                <div class="candidate-contact-item">
                    <i class="fas fa-phone"></i>
                    <span>${escapeHTML(profile.phone || "Phone not available")}</span>
                </div>

                <div class="candidate-contact-item">
                    <i class="fas fa-map-marker-alt"></i>
                    <span>${escapeHTML(profile.location || "Location not available")}</span>
                </div>

                <div class="candidate-contact-item">
                    <i class="fab fa-linkedin"></i>
                    <span>${escapeHTML(profile.linkedin || "LinkedIn not available")}</span>
                </div>

                <div class="candidate-contact-item">
                    <i class="fab fa-github"></i>
                    <span>${escapeHTML(profile.github || "GitHub not available")}</span>
                </div>

            </div>

            <div class="candidate-profile-section-inner">
                <h3><i class="fas fa-user-circle"></i> Profile Summary</h3>

                <p class="candidate-summary">
                    ${escapeHTML(profile.profile_summary || "Profile summary not available.")}
                </p>
            </div>

            <div class="candidate-profile-section-inner">
                <h3><i class="fas fa-graduation-cap"></i> Education</h3>

                <div class="candidate-education-list">
                    ${educationHTML}
                </div>
            </div>

        </div>
    `;
}




function renderScoreBreakdown(candidate) {

    const components = candidate.component_breakdown || [];
    const weights = candidate.scoring_structure?.normalized_weights || {};

    const labels = {
        required_skills: "Required Skills",
        preferred_skills: "Preferred Skills",
        responsibilities: "Responsibilities",
        relevant_experience: "Relevant Experience",
        education: "Education"
    };

    const breakdownHTML = components.map(component => {

        const score = Number(component.score || 0);
        const label = labels[component.component] || component.component;
        const weight = weights[component.component];

        return `
            <div class="score-component-card">

                <div class="score-component-header">
                    <span class="score-component-name">
                        ${label}
                    </span>

                    <span class="score-component-value">
                        ${score.toFixed(1)}%
                    </span>
                </div>

                <div class="score-progress-track">
                    <div class="score-progress-fill"
                         style="width: ${Math.max(0, Math.min(100, score))}%">
                    </div>
                </div>

                <div class="score-component-footer">
                    <span>Match: ${score.toFixed(1)}%</span>
                    ${weight !== undefined
                        ? `<span>Weight: ${Number(weight).toFixed(2)}%</span>`
                        : ""
                    }
                </div>

            </div>
        `;

    }).join("");

    const overallScore = Number(candidate.overall_score || 0);

    const content = document.getElementById("candidateAnalysisContent");

    content.insertAdjacentHTML("beforeend", `
        <div class="candidate-score-section">

            <div class="overall-score-card">

                <div>
                    <h3>Overall Match Score</h3>
                    <p>Candidate's weighted evaluation</p>
                </div>

                <div class="overall-score-value">
                    ${overallScore.toFixed(2)}%
                </div>

            </div>

            <div class="score-breakdown-container">

                <h3>Score Breakdown</h3>

                <div class="score-components-grid">
                    ${breakdownHTML}
                </div>

            </div>

        </div>
    `);
}
















function renderSkillsAnalysis(candidate) {

    const components = candidate.component_breakdown || [];

    const required = components.find(
        c => c.component === "required_skills"
    ) || {};

    const preferred = components.find(
        c => c.component === "preferred_skills"
    ) || {};

    function escapeHTML(value) {
        return String(value ?? "").replace(/[&<>"']/g, char => ({
            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
            '"': "&quot;",
            "'": "&#39;"
        }[char]));
    }

    function renderSkillList(items, type) {

        if (!items || items.length === 0) {
            return `<p class="skill-empty">No skills to display.</p>`;
        }

        return items.map(item => {

            const skillName =
                typeof item === "string"
                    ? item
                    : item.skill || item.name || "Unnamed skill";

            const evidence =
                typeof item === "object"
                    ? item.evidence || item.reason || ""
                    : "";

            const method =
                typeof item === "object"
                    ? item.method || ""
                    : "";

            return `
                <div class="skill-analysis-item ${type}">

                    <div class="skill-analysis-header">
                        <span class="skill-analysis-name">
                            ${escapeHTML(skillName)}
                        </span>

                        <span class="skill-status-badge ${type}">
                            ${type === "matched" ? "Matched" : "Not found"}
                        </span>
                    </div>

                    ${method ? `
                        <p class="skill-method">
                            Match method: ${escapeHTML(method)}
                        </p>
                    ` : ""}

                    ${evidence ? `
                        <div class="skill-evidence">
                            <span class="skill-evidence-label">Resume Evidence</span>
                            <p>${escapeHTML(evidence)}</p>
                        </div>
                    ` : ""}

                </div>
            `;

        }).join("");
    }

    function renderSkillComponent(component, title) {

        const matched = component.matched_evidence || [];
        const missing = component.missing_evidence || [];

        return `
            <div class="skill-category-section">

                <h3>${title}</h3>

                <div class="skills-analysis-columns">

                    <div class="skills-column">

                        <h4>
                            <i class="fas fa-check-circle"></i>
                            Matched Skills (${matched.length})
                        </h4>

                        ${renderSkillList(matched, "matched")}

                    </div>

                    <div class="skills-column">

                        <h4>
                            <i class="fas fa-exclamation-circle"></i>
                            Missing Skills (${missing.length})
                        </h4>

                        ${renderSkillList(missing, "missing")}

                    </div>

                </div>

            </div>
        `;
    }

    const content = document.getElementById("candidateAnalysisContent");

    content.insertAdjacentHTML("beforeend", `
        <div class="candidate-skills-analysis">

            <h3 class="skills-analysis-main-title">
                <i class="fas fa-tools"></i>
                Skills Analysis
            </h3>

            ${renderSkillComponent(required, "Required Skills")}

            ${renderSkillComponent(preferred, "Preferred Skills")}

            <p class="skills-disclaimer">
                Missing skills indicate that supporting evidence was not
                identified in the resume. They do not necessarily mean
                the candidate lacks the skill.
            </p>

        </div>
    `);
}









function renderResponsibilitiesAnalysis(candidate) {

    const components = candidate.component_breakdown || [];

    const responsibilityComponent = components.find(
        c => c.component === "responsibilities"
    ) || {};

    const fullyMatched = responsibilityComponent.matched_evidence || [];
    const partiallyMatched = responsibilityComponent.partial_evidence || [];
    const missing = responsibilityComponent.missing_evidence || [];

    function escapeHTML(value) {
        return String(value ?? "").replace(/[&<>"']/g, char => ({
            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
            '"': "&quot;",
            "'": "&#39;"
        }[char]));
    }

    function getText(item) {
        if (typeof item === "string") return item;

        return item.responsibility ||
            item.requirement ||
            item.text ||
            item.description ||
            item.evidence ||
            "Responsibility";
    }

    function getEvidence(item) {
        if (typeof item === "string") return "";

        return item.evidence ||
            item.reason ||
            item.explanation ||
            "";
    }

    function renderItems(items, type, label) {

        if (!items.length) {
            return `<p class="responsibility-empty">No items in this category.</p>`;
        }

        return items.map(item => {

            const text = getText(item);
            const evidence = getEvidence(item);

            return `
                <div class="responsibility-item ${type}">

                    <div class="responsibility-item-header">
                        <strong>${escapeHTML(text)}</strong>

                        <span class="responsibility-status ${type}">
                            ${label}
                        </span>
                    </div>

                    ${evidence ? `
                        <div class="responsibility-evidence">
                            <span>Supporting Evidence</span>
                            <p>${escapeHTML(evidence)}</p>
                        </div>
                    ` : ""}

                </div>
            `;

        }).join("");
    }

    const content = document.getElementById("candidateAnalysisContent");

    content.insertAdjacentHTML("beforeend", `
        <div class="responsibility-analysis-section">

            <h3 class="responsibility-main-title">
                <i class="fas fa-tasks"></i>
                Responsibilities Analysis
            </h3>

            <div class="responsibility-category">

                <h4>
                    <i class="fas fa-check-circle"></i>
                    Fully Supported (${fullyMatched.length})
                </h4>

                ${renderItems(fullyMatched, "fully-matched", "Fully Supported")}

            </div>

            <div class="responsibility-category">

                <h4>
                    <i class="fas fa-adjust"></i>
                    Partially Supported (${partiallyMatched.length})
                </h4>

                ${renderItems(partiallyMatched, "partially-matched", "Partially Supported")}

            </div>

            <div class="responsibility-category">

                <h4>
                    <i class="fas fa-exclamation-circle"></i>
                    Not Found (${missing.length})
                </h4>

                ${renderItems(missing, "not-found", "Not Found")}

            </div>

            <p class="responsibility-disclaimer">
                Responsibilities are evaluated using semantic similarity
                and evidence extracted from the resume. Not found means
                supporting evidence was not identified.
            </p>

        </div>
    `);
}



function escapeHTML(value) {
    return String(value ?? "")
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#39;");
}



function renderExperienceAnalysis(candidate) {

    const component = candidate.component_breakdown?.find(
        c => c.component === "relevant_experience"
    );

    if (!component) {
        return;
    }

    const records = component.matched_evidence || [];
    const missing = component.missing_evidence || [];

    const html = `
        <section class="candidate-experience-section">

            <div class="analysis-section-heading">
                <h3><i class="fas fa-briefcase"></i> Experience Analysis</h3>
                <p>Employment history and job relevance evaluation</p>
            </div>

            <div class="experience-summary-card">
                <div>
                    <span class="experience-summary-label">Experience Match Score</span>
                    <h2>${Number(component.score || 0).toFixed(2)}%</h2>
                </div>
                <div>
                    <span class="experience-summary-label">Component Weight</span>
                    <h2>${Number(component.weight || 0).toFixed(2)}%</h2>
                </div>
                <div>
                    <span class="experience-summary-label">Weighted Contribution</span>
                    <h2>${Number(component.contribution || 0).toFixed(2)}</h2>
                </div>
            </div>

            <div class="experience-evaluation-reason">
                <strong>Evaluation:</strong>
                <p>${escapeHTML(component.reason || "No evaluation reason available.")}</p>
            </div>

            <div class="experience-records-container">

                ${
                    records.length > 0
                    ? records.map(record => {

                        const relevance = record.relevance_level || "unknown";

                        const relevanceLabel = relevance.replace(/_/g, " ");

                        const duration = Number(record.duration_months || 0);

                        const relevanceWeight = Number(record.relevance_weight || 0);

                        const weightedDuration = duration * relevanceWeight;

                        return `
                            <div class="experience-record-card">

                                <div class="experience-record-header">
                                    <div>
                                        <h4>${escapeHTML(record.job_title || "Job Title Not Available")}</h4>
                                        <p>${escapeHTML(record.company_name || "Company Not Available")}</p>
                                    </div>

                                    <span class="experience-relevance-badge ${relevance}">
                                        ${escapeHTML(relevanceLabel)}
                                    </span>
                                </div>

                                <div class="experience-record-meta">
                                    <span>
                                        <i class="fas fa-calendar"></i>
                                        ${escapeHTML(record.start_date || "N/A")} – ${escapeHTML(record.end_date || "N/A")}
                                    </span>

                                    <span>
                                        <i class="fas fa-clock"></i>
                                        ${duration} month${duration !== 1 ? "s" : ""}
                                    </span>

                                    <span>
                                        <i class="fas fa-balance-scale"></i>
                                        Relevance weight: ${relevanceWeight}
                                    </span>
                                </div>

                                <div class="experience-duration-comparison">

                                    <div>
                                        <span>Actual Duration</span>
                                        <strong>${duration} months</strong>
                                    </div>

                                    <div>
                                        <span>Weighted Duration</span>
                                        <strong>${weightedDuration.toFixed(1)} months</strong>
                                    </div>

                                </div>

                                ${
                                    record.relevance_reason
                                    ? `
                                        <div class="experience-relevance-reason">
                                            <strong>Why this experience was evaluated this way</strong>
                                            <p>${escapeHTML(record.relevance_reason)}</p>
                                        </div>
                                    `
                                    : ""
                                }

                                ${
                                    record.evidence
                                    ? `
                                        <div class="experience-evidence">
                                            <strong>Resume Evidence</strong>
                                            <p>${escapeHTML(record.evidence)}</p>
                                        </div>
                                    `
                                    : ""
                                }

                            </div>
                        `;

                    }).join("")
                    : `
                        <div class="experience-empty-state">
                            No relevant employment records were identified.
                        </div>
                    `
                }

            </div>

            ${
                missing.length > 0
                ? `
                    <div class="experience-missing-section">
                        <h4>Experience Not Evaluated / Missing</h4>
                        ${missing.map(item => `
                            <div class="experience-missing-item">
                                ${escapeHTML(typeof item === "string" ? item : JSON.stringify(item))}
                            </div>
                        `).join("")}
                    </div>
                `
                : ""
            }

            <div class="experience-disclaimer">
                Experience relevance is estimated using resume evidence and the job description.
                Weighted duration adjusts actual employment duration based on role relevance.
            </div>

        </section>
    `;

    const content = document.getElementById("candidateAnalysisContent");

    content.insertAdjacentHTML("beforeend", html);
}




// Candidate Analysis Modal Controls

document.addEventListener("click", function (event) {

    // Open modal
    const viewButton = event.target.closest(".view-candidate-btn");

    if (viewButton) {

        const candidateId = viewButton.dataset.candidateId;

        const candidate = evaluatedCandidates.find(
            c => c.candidate_id === candidateId
        );

        if (!candidate) {
            alert("Candidate data not found.");
            return;
        }

        console.log("Selected candidate for analysis:", candidate);
        console.log(
    "Experience component data:",
    candidate.component_breakdown?.find(
        c => c.component === "relevant_experience"
    )
);
      renderCandidateProfile(candidate);
      renderScoreBreakdown(candidate);
      renderSkillsAnalysis(candidate);
      renderResponsibilitiesAnalysis(candidate);
      renderExperienceAnalysis(candidate);
        const modal = document.getElementById("candidateAnalysisModal");

        if (modal) {
            modal.classList.remove("hidden");
        }

        return;
    }

    // Close using the X button
    if (event.target.closest("#closeCandidateModal")) {

        const modal = document.getElementById("candidateAnalysisModal");

        if (modal) {
            modal.classList.add("hidden");
        }

        return;
    }

    // Close when clicking the backdrop
    const modal = document.getElementById("candidateAnalysisModal");

    if (modal && event.target === modal) {
        modal.classList.add("hidden");
    }

});


// Close modal using Escape
document.addEventListener("keydown", function (event) {

    if (event.key === "Escape") {

        const modal = document.getElementById("candidateAnalysisModal");

        if (modal && !modal.classList.contains("hidden")) {
            modal.classList.add("hidden");
        }

    }

});








/* ==========================================
   HIREPULSE DETAILED PDF REPORT
========================================== */

function downloadDetailedReport(candidates) {

    if (!window.jspdf || !window.jspdf.jsPDF) {
        alert("PDF library not loaded. Please refresh the page.");
        return;
    }

    if (!candidates || candidates.length === 0) {
        alert("No candidate results available.");
        return;
    }

    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    const pageWidth = doc.internal.pageSize.getWidth();
    const pageHeight = doc.internal.pageSize.getHeight();
    const margin = 15;

    let y = 20;

    const jdRecord = JSON.parse(
        sessionStorage.getItem("hirepulse_jd") || "{}"
    );

    const jdData = jdRecord.extracted_requirements || {};

    function clean(value) {
        if (value === null || value === undefined) return "N/A";

        if (typeof value === "object") {
            if (Array.isArray(value)) {
                return value.map(clean).join(", ");
            }

            return Object.entries(value)
                .map(([key, val]) => `${key}: ${clean(val)}`)
                .join("; ");
        }

        return String(value);
    }

    function addPageIfNeeded(height = 25) {
        if (y + height > pageHeight - 20) {
            doc.addPage();
            y = 20;
        }
    }

    function addTitle(text) {
        addPageIfNeeded(30);

        doc.setFont("helvetica", "bold");
        doc.setFontSize(13);
        doc.text(text, margin, y);

        y += 8;
    }

    function addText(text, fontSize = 9) {
        const content = clean(text);

        doc.setFont("helvetica", "normal");
        doc.setFontSize(fontSize);

        const lines = doc.splitTextToSize(
            content,
            pageWidth - margin * 2
        );

        addPageIfNeeded(lines.length * 5 + 5);

        doc.text(lines, margin, y);

        y += lines.length * 5 + 4;
    }

    function addTable(headers, rows) {
        if (!rows || rows.length === 0) {
            addText("No data available.");
            return;
        }

        doc.autoTable({
            startY: y,
            head: [headers],
            body: rows,
            margin: {
                left: margin,
                right: margin
            },
            theme: "grid",
            styles: {
                fontSize: 8,
                cellPadding: 3,
                overflow: "linebreak"
            },
            headStyles: {
                fillColor: [91, 65, 155]
            },
            columnStyles: {
                0: {
                    cellWidth: 40
                }
            }
        });

        y = doc.lastAutoTable.finalY + 10;
    }

    function addEvidenceSection(title, component) {

        if (!component) return;

        addTitle(title);

        addText(
            `Score: ${Number(component.score || 0).toFixed(2)}%`
        );

        addText(
            `Weight: ${component.weight ?? "N/A"}%`
        );

        addText(
            `Contribution: ${component.contribution ?? "N/A"}`
        );

        addText(
            `Reason: ${component.reason || "No explanation available."}`
        );

        const matched = component.matched_evidence || [];
        const missing = component.missing_evidence || [];

        if (matched.length) {
            addText("Matched Evidence:");

            addTable(
                ["Requirement", "Evidence / Details"],
                matched.map(item => [
                    clean(
                        item.skill ||
                        item.responsibility ||
                        item.job_title ||
                        item.name ||
                        item.component ||
                        "Matched Item"
                    ),
                    clean(
                        item.evidence ||
                        item.description ||
                        item.reason ||
                        item.relevance_reason ||
                        item
                    )
                ])
            );
        }

        if (missing.length) {
            addText("Missing / Unmatched Evidence:");

            addTable(
                ["Requirement", "Details"],
                missing.map(item => [
                    clean(
                        item.skill ||
                        item.responsibility ||
                        item.name ||
                        "Requirement"
                    ),
                    clean(
                        item.reason ||
                        item.evidence ||
                        item
                    )
                ])
            );
        }
    }

    /* Cover / Screening Summary */

    doc.setFont("helvetica", "bold");
    doc.setFontSize(22);
    doc.text("HirePulse", margin, y);

    y += 10;

    doc.setFontSize(16);
    doc.text("Detailed Screening Report", margin, y);

    y += 12;

    doc.setFont("helvetica", "normal");
    doc.setFontSize(10);

    addText(`Report Date: ${new Date().toLocaleDateString()}`);
    addText(`Candidates Evaluated: ${candidates.length}`);

    addText(
        `Job Title: ${
            jdData.job_title ||
            jdData.title ||
            "Not specified"
        }`
    );

    addText(
        `Company: ${
            jdData.company_name ||
            "Not specified"
        }`
    );

    addText(
        `Required Experience: ${
            jdData.minimum_experience_years ??
            jdData.min_experience_years ??
            "Not specified"
        } years`
    );

    addTitle("Candidate Ranking");

    addTable(
        ["Rank", "Candidate", "Score", "Filename"],
        candidates.map((c, i) => [
            `#${c.rank || i + 1}`,
            clean(c.candidate_profile?.candidate_name || "Unknown"),
            `${Number(c.overall_score || 0).toFixed(2)}%`,
            clean(c.filename)
        ])
    );


    /* Detailed Candidate Reports */

    candidates.forEach((candidate, index) => {

        doc.addPage();
        y = 20;

        const profile = candidate.candidate_profile || {};
        const components = candidate.component_breakdown || [];

        const candidateName =
            profile.candidate_name ||
            candidate.filename ||
            `Candidate ${index + 1}`;

        doc.setFont("helvetica", "bold");
        doc.setFontSize(18);

        doc.text(
            `Rank #${candidate.rank || index + 1} - ${candidateName}`,
            margin,
            y
        );

        y += 12;

        addText(`Overall Match Score: ${Number(candidate.overall_score || 0).toFixed(2)}%`);

        addText(`Resume File: ${candidate.filename || "N/A"}`);

        /* Profile */

        addTitle("Candidate Profile");

        addTable(
            ["Field", "Details"],
            [
                ["Name", profile.candidate_name],
                ["Email", profile.email],
                ["Phone", profile.phone],
                ["Location", profile.location],
                ["Professional Title", profile.professional_title],
                ["LinkedIn", profile.linkedin],
                ["GitHub", profile.github],
                ["Portfolio", profile.portfolio],
                ["Other Links", profile.other_links],
                ["Summary", profile.profile_summary]
            ].map(row => row.map(clean))
        );

        /* Education */

        addTitle("Education");

        const education = profile.education || [];

        if (Array.isArray(education) && education.length) {
            addTable(
                ["Education Details"],
                education.map(item => [clean(item)])
            );
        } else {
            addText(clean(education));
        }

        /* Score Breakdown */

        addTitle("Score Breakdown");

        addTable(
            ["Component", "Score", "Weight", "Contribution", "Status"],
            components.map(c => [
                clean(c.component),
                `${Number(c.score || 0).toFixed(2)}%`,
                `${c.weight ?? "N/A"}%`,
                clean(c.contribution),
                clean(c.status)
            ])
        );

        /* Required Skills */

        const requiredSkills = components.find(
            c => c.component === "required_skills"
        );

        addEvidenceSection(
            "Required Skills Evaluation",
            requiredSkills
        );

        /* Preferred Skills */

        const preferredSkills = components.find(
            c => c.component === "preferred_skills"
        );

        addEvidenceSection(
            "Preferred Skills Evaluation",
            preferredSkills
        );

        /* Responsibilities */

        const responsibilities = components.find(
            c => c.component === "responsibilities"
        );

        addEvidenceSection(
            "Responsibility Evaluation",
            responsibilities
        );

        /* Experience */

        const experience = components.find(
            c => c.component === "relevant_experience"
        );

        if (experience) {

            addTitle("Relevant Experience Evaluation");

            addText(`Score: ${experience.score ?? 0}%`);

            addText(`Weight: ${experience.weight ?? "N/A"}%`);

            addText(`Contribution: ${experience.contribution ?? "N/A"}`);

            addText(`Reason: ${experience.reason || "N/A"}`);

            const records = experience.matched_evidence || [];

            if (records.length) {

                addTitle("Employment Records");

                addTable(
                    [
                        "Role / Company",
                        "Duration",
                        "Relevance",
                        "Weighted Months",
                        "Reason / Evidence"
                    ],
                    records.map(record => [
                        `${clean(record.job_title)}\n${clean(record.company_name)}`,
                        `${clean(record.start_date)} - ${clean(record.end_date)}\n${clean(record.duration_months)} months`,
                        `${clean(record.relevance_level)} (${clean(record.relevance_weight)})`,
                        clean(record.weighted_duration_months),
                        `${clean(record.relevance_reason)}\n${clean(record.evidence)}`
                    ])
                );
            }

            if (experience.missing_evidence?.length) {
                addTitle("Experience Missing Evidence");

                addTable(
                    ["Details"],
                    experience.missing_evidence.map(item => [
                        clean(item)
                    ])
                );
            }
        }

    });


    /* Page Numbers */

    const totalPages = doc.internal.getNumberOfPages();

    for (let i = 1; i <= totalPages; i++) {

        doc.setPage(i);

        doc.setFont("helvetica", "normal");
        doc.setFontSize(8);

        doc.text(
            `HirePulse | Detailed Screening Report | Page ${i} of ${totalPages}`,
            pageWidth / 2,
            pageHeight - 10,
            { align: "center" }
        );
    }


    /* Download */

    const fileName = `HirePulse_Report_${new Date()
        .toISOString()
        .slice(0, 10)}.pdf`;

    doc.save(fileName);
}


/* Connect the Download Report button */

document.addEventListener("click", function (event) {

    if (event.target.closest("#downloadReportBtn")) {
        downloadDetailedReport(evaluatedCandidates);
    }

});

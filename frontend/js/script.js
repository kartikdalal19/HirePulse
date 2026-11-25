// const newScreeningBtn = document.getElementById("newScreeningBtn");
// const startAnalysisBtn = document.getElementById("startAnalysisBtn");

// function openScreening() {
//     alert("The screening interface will be implemented in the next step.");
// }

// newScreeningBtn.addEventListener("click", openScreening);
// startAnalysisBtn.addEventListener("click", openScreening);
const newScreeningBtn = document.getElementById("newScreeningBtn");
const startAnalysisBtn = document.getElementById("startAnalysisBtn");

function openScreening() {
    window.location.href = "screening.html";
}

newScreeningBtn.addEventListener("click", openScreening);
startAnalysisBtn.addEventListener("click", openScreening);
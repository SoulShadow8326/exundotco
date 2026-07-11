const addBtn = document.querySelector(".add-btn");
const themeToggle = document.querySelector("#themeToggle"); /* For Dark mode/Light Mode Button */
const modal = document.querySelector("#addModal");
const cancelBtn = document.querySelector(".cancel-btn");

const slugInput = document.querySelector("#slugInput");
const urlInput = document.querySelector("#urlInput");
const saveBtn = document.querySelector(".save-btn");

const tableBody = document.querySelector("#tableBody");

// Open Modal
addBtn.addEventListener("click", () => {
    modal.style.display = "flex";
});

// Close Modal
cancelBtn.addEventListener("click", () => {
    modal.style.display = "none";
});

// Close Modal when clicking outside
modal.addEventListener("click", (event) => {
    if (event.target === modal) {
        modal.style.display = "none";
    }
});

// Add Link
saveBtn.addEventListener("click", () => {

    let slug = slugInput.value.trim();

    // Remove exun.co/ if user enters it
    slug = slug.replace(/^exun\.co\//, "");

    const url = urlInput.value.trim();

    // Empty field validation
    if (!slug || !url) {
        alert("Please enter both Slug and URL.");
        return;
    }

    // URL validation
    try {
        new URL(url);
    } catch {
        alert("Please enter a valid URL.");
        return;
    }

    // Duplicate slug validation
    const existingSlugs = tableBody.querySelectorAll("tr td:first-child");

    for (const cell of existingSlugs) {
        if (cell.textContent === `exun.co/${slug}`) {
            alert("This slug already exists.");
            return;
        }
    }

    // Create Row
    const newRow = document.createElement("tr");

    // Slug Cell
    const slugCell = document.createElement("td");
    slugCell.textContent = `exun.co/${slug}`;

    // URL Cell
    const urlCell = document.createElement("td");

    const link = document.createElement("a");
    link.href = url;
    link.textContent = url;
    link.target = "_blank";
    link.rel = "noopener noreferrer";

    urlCell.appendChild(link);

    // Date Cell
    const dateCell = document.createElement("td");

    const createdAt = new Date().toLocaleDateString("en-US", {
        month: "long",
        day: "numeric",
        year: "numeric"
    });

    dateCell.textContent = createdAt;

    // Action Cell
    const actionCell = document.createElement("td");

    const buttonContainer = document.createElement("div");
    buttonContainer.className = "button-container";

    const editBtn = document.createElement("button");
    editBtn.textContent = "Edit";
    editBtn.className = "edit-btn";

    const deleteBtn = document.createElement("button");
    deleteBtn.textContent = "Delete";
    deleteBtn.className = "delete-btn";

    buttonContainer.appendChild(editBtn);
    buttonContainer.appendChild(deleteBtn);

    actionCell.appendChild(buttonContainer);

    // Assemble Row
    newRow.appendChild(slugCell);
    newRow.appendChild(urlCell);
    newRow.appendChild(dateCell);
    newRow.appendChild(actionCell);

    // Add Row to Table
    tableBody.appendChild(newRow);

    // Clear Inputs
    slugInput.value = "";
    urlInput.value = "";

    // Close Modal
    modal.style.display = "none";
});

themeToggle.addEventListener("change", () => { /* Checks for theme toogle box being On or Off */

    document.body.classList.toggle("dark-mode");

});
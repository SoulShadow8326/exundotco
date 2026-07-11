const addBtn = document.querySelector(".add-btn");
const modal = document.querySelector("#addModal");
const cancelBtn = document.querySelector(".cancel-btn");

const slugInput = document.querySelector("#slugInput");
const urlInput = document.querySelector("#urlInput");
const saveBtn = document.querySelector(".save-btn");

const tableBody = document.querySelector("#tableBody");
let isEditing = false;
let editingRow = null;

// Open Modal
addBtn.addEventListener("click", () => {
    modal.style.display = "flex";
});

// Close Modal
cancelBtn.addEventListener("click", () => {

    modal.style.display = "none";

    slugInput.value = "";
    urlInput.value = "";

    isEditing = false;
    editingRow = null;

    saveBtn.textContent = "Add Link";
    document.querySelector(".modal-content h2").textContent = "Add New Link";

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

        if (
            cell.textContent === `exun.co/${slug}` &&
            (!isEditing || cell.parentElement !== editingRow)
        ) {
            alert("This slug already exists.");
            return;
        }

    }

    // EDIT EXISTING ROW
    if (isEditing) {

        editingRow.cells[0].textContent = `exun.co/${slug}`;

        const link = editingRow.cells[1].querySelector("a");
        link.href = url;
        link.textContent = url;

        modal.style.display = "none";

        slugInput.value = "";
        urlInput.value = "";

        isEditing = false;
        editingRow = null;

        saveBtn.textContent = "Add Link";
        document.querySelector(".modal-content h2").textContent = "Add New Link";

        return;
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

tableBody.addEventListener("click", (event) => {

    // DELETE
    if (event.target.classList.contains("delete-btn")) {

        const row = event.target.closest("tr");

        if (confirm("Are you sure you want to delete this link?")) {
            row.remove();
        }

    }

    // EDIT
    if (event.target.classList.contains("edit-btn")) {

        editingRow = event.target.closest("tr");
        isEditing = true;

        const slug = editingRow.cells[0].textContent.replace("exun.co/", "");
        const url = editingRow.cells[1].querySelector("a").href;

        slugInput.value = slug;
        urlInput.value = url;

        document.querySelector(".modal-content h2").textContent = "Edit Link";
        saveBtn.textContent = "Save Changes";

        modal.style.display = "flex";
    }

});
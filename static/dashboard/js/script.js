const addBtn = document.querySelector(".add-btn");
const themeToggle =
  document.querySelector("#themeToggle"); /* For Dark mode/Light Mode Button */
const modal = document.querySelector("#addModal");
const cancelBtn = document.querySelector(".cancel-btn");
const slugInput = document.querySelector("#slugInput");
const urlInput = document.querySelector("#urlInput");
const saveBtn = document.querySelector(".save-btn");
const searchInput = document.querySelector("#searchInput");
const tableBody = document.querySelector("#tableBody");
let isEditing = false;
let editingRow = null;

function formatDate(timestamp) {
  return new Date(timestamp * 1000).toLocaleString("en-GB", {
    day: "2-digit",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  });
}

function createTableRow(link) {
  const newRow = document.createElement("tr");

  // Slug Cell
  const slugCell = document.createElement("td");
  slugCell.textContent = `exun.co${link.slug}`;

  // URL Cell
  const urlCell = document.createElement("td");

  const anchor = document.createElement("a");
  anchor.href = link.url;
  anchor.textContent = link.url;
  anchor.target = "_blank";
  anchor.rel = "noopener noreferrer";

  urlCell.appendChild(anchor);

  // Date Cell
  const dateCell = document.createElement("td");

  dateCell.textContent = formatDate(link.date_modified);
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

  newRow.appendChild(slugCell);
  newRow.appendChild(urlCell);
  newRow.appendChild(dateCell);
  newRow.appendChild(actionCell);

  tableBody.appendChild(newRow);
}

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
  modal.querySelector("h2").textContent = "Add New Link";
});

// Close Modal when clicking outside
modal.addEventListener("click", (event) => {
  if (event.target === modal) {
    modal.style.display = "none";
    slugInput.value = "";
    urlInput.value = "";
    isEditing = false;
    editingRow = null;
    saveBtn.textContent = "Add Link";
    modal.querySelector("h2").textContent = "Add New Link";
  }
});

// Add Link
saveBtn.addEventListener("click", async () => {
  let slug = slugInput.value.trim();

  // Remove exun.co/ if user enters it
  slug = slug.replace(/^exun\.co\//, "");
  slug = slug.replace(/^\/+/, "");
  // Slug validation
  const slugPattern = /^[A-Za-z0-9/]+$/;

  if (!slugPattern.test(slug)) {
    //Check If Slug Is following pattern Firt Time seeing != not
    alert(
      "Current SLug Is Invalid. Slugs can only contain letters, numbers and forward slashes (/).",
    );
    return;
  }

  const url = urlInput.value.trim(); /* Valid Url Checker */

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

  if (isEditing) {
    const oldSlug = "/" + editingRow.cells[0].textContent.replace(/^exun\.co\//, "").replace(/^\/+/, "");
    const payload = {
      slug: oldSlug,
      new_slug: `/${slug}`,
      new_url: url,
    };
    try {
      const response = await fetch("/api/update", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });
      const data = await response.json();
      if (data.success) {
        editingRow.cells[0].textContent = `exun.co/${slug}`;
        const anchor = editingRow.cells[1].querySelector("a");
        anchor.href = url;
        anchor.textContent = url;
        editingRow.cells[2].textContent = formatDate(Date.now() / 1000);
      } else {
        alert(data.message);
      }
    } catch (error) {
      console.error(error);
      alert("Failed to update link. Please try again.");
    }
  } else {
    const payload = { slug: `/${slug}`, url: url };
    try {
      const response = await fetch("/api/create", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });
      const data = await response.json();
      console.log(data);
      if (data.success) {
        createTableRow({
          slug: `/${slug}`,
          url: url,
          date_modified: Date.now() / 1000,
        });
      } else {
        alert(data.message);
      }
    } catch (error) {
      console.error("Error adding link:", error);
      alert("Failed to add link. Please try again.");
    }
  }

  slugInput.value = "";
  urlInput.value = "";
  isEditing = false;
  editingRow = null;
  saveBtn.textContent = "Add Link";
  modal.querySelector("h2").textContent = "Add New Link";
  modal.style.display = "none";
});

tableBody.addEventListener("click", async (event) => {
  if (event.target.classList.contains("delete-btn")) {
    const row = event.target.closest("tr");
    const slug = "/" + row.cells[0].textContent.replace(/^exun\.co\//, "").replace(/^\/+/, "");
    if (confirm("Are you sure you want to delete this link?")) {
      try {
        const response = await fetch("/api/delete", {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ slug: slug }),
        });
        const data = await response.json();
        if (data.success) {
          row.remove();
          const rows = tableBody.querySelectorAll("tr:not(#noResultsRow)");
          if (rows.length === 0) {
            noResultsRow.style.display = "";
          }
        } else {
          alert(data.message);
        }
      } catch (error) {
        console.error(error);
        alert("Failed to delete link. Please try again.");
      }
    }
  }

  if (event.target.classList.contains("edit-btn")) {
    editingRow = event.target.closest("tr");
    isEditing = true;
    const slug = editingRow.cells[0].textContent.replace(/^exun\.co\//, "").replace(/^\/+/, "");
    const url = editingRow.cells[1].querySelector("a").href;
    slugInput.value = slug;
    urlInput.value = url;
    modal.querySelector("h2").textContent = "Edit Link";
    saveBtn.textContent = "Save Changes";
    modal.style.display = "flex";
  }
});

themeToggle.addEventListener("change", () => {
  /* Checks for theme toogle box being On or Off */

  document.body.classList.toggle("dark-mode");

  localStorage.setItem(
    "theme",
    document.body.classList.contains("dark-mode") ? "dark" : "light",
  );
});

// search

let noResultsRow = document.querySelector("#noResultsRow");

searchInput.addEventListener("input", () => {
  const searchText = searchInput.value.toLowerCase().trim();

  const rows = tableBody.querySelectorAll("tr:not(#noResultsRow)");

  let matchFound = false;

  rows.forEach((row) => {
    const slug = row.cells[0].textContent.toLowerCase();
    const url = row.cells[1].textContent.toLowerCase();

    if (slug.includes(searchText) || url.includes(searchText)) {
      row.style.display = "";
      matchFound = true;
    } else {
      row.style.display = "none";
    }
  });

  if (matchFound) {
    noResultsRow.style.display = "none";
  } else {
    noResultsRow.style.display = "";
  }
});
window.addEventListener("DOMContentLoaded", async () => {
  const savedTheme = localStorage.getItem("theme");

  if (savedTheme === "dark") {
    document.body.classList.add("dark-mode");
    themeToggle.checked = true;
  }
  try {
    const response = await fetch("/api/getAll");
    const data = await response.json();

    if (!data.success) {
      alert(data.message);
      return;
    }

    tableBody.innerHTML = `<tr id="noResultsRow" style="display:none;">
    <td colspan="4" class="no-results">
        No matching links found.
    </td>
</tr>`;
    noResultsRow = document.querySelector("#noResultsRow");
    data.links.forEach((link) => {
      createTableRow(link);
    });
  } catch (error) {
    console.error(error);
    alert("Failed to load links.");
  }
});

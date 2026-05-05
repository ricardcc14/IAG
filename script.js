async function generateLogo(brand_name, style, colors) {
    const res = await fetch("http://localhost:3000/api/logo", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            brand_name: brand_name,
            style: style,
            colors: colors
        })
    });
    const data = await res.json();
    document.getElementById("logo-img").src = `data:image/png;base64,${data.image_base64}`;
}

async function generatePalette() {
    const res = await fetch("http://localhost:3000/api/palette", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            brand_name: document.getElementById("name").value,
            style: "minimalist"
        })
    });
    const data = await res.json();
    const palette = JSON.parse(data.palette);
    console.log(palette); // array de 5 hex codes
}

async function uploadFile(input) {
    const file = input.files[0];
    if (!file) return;

    // Validation
    const allowedExtensions = ['.png', '.svg', '.ai', '.jpg', '.jpeg'];
    const fileExtension = '.' + file.name.split('.').pop().toLowerCase();

    if (!allowedExtensions.includes(fileExtension)) {
        alert(`Invalid file type. Please upload: ${allowedExtensions.join(', ')}`);
        input.value = '';
        return;
    }

    const maxSize = 5 * 1024 * 1024; // 5MB
    if (file.size > maxSize) {
        alert(`File too large! Maximum size is 5MB. Your file: ${(file.size / 1024 / 1024).toFixed(2)}MB`);
        input.value = '';
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
        const res = await fetch("http://localhost:3000/api/upload", {
            method: "POST",
            body: formData
        });
        const data = await res.json();

        if (data.error) {
            alert("Error: " + data.error);
            return;
        }

        console.log("File uploaded:", data);
        
        // Refresh sidebar
        loadFiles();

        // Update preview for images
        if (file.type.startsWith("image/")) {
            const reader = new FileReader();
            reader.onload = (e) => {
                const img = document.querySelector(".logo-preview img");
                if (img) {
                    img.src = e.target.result;
                    img.style.opacity = "1";
                }
            };
            reader.readAsDataURL(file);
        }
    } catch (err) {
        console.error("Upload failed:", err);
        alert("Upload failed. Make sure the server is running on port 3000.");
    }
}

async function loadFiles() {
    const fileList = document.getElementById("sidebar-file-list");
    if (!fileList) return;

    try {
        const res = await fetch("http://localhost:3000/api/files");
        const data = await res.json();

        if (data.files && data.files.length > 0) {
            fileList.innerHTML = data.files.map(file => `
                <div class="file-item">
                    <div class="file-info" onclick="selectFile('${file}')">
                        <img src="Assets/DesignBrandIcon.svg" style="width: 14px; opacity: 0.5;">
                        <span title="${file}">${file}</span>
                    </div>
                    <button class="btn-delete" onclick="deleteFile('${file}')">DELETE</button>
                </div>
            `).join("");
        } else {
            fileList.innerHTML = '<p class="empty-msg">No files uploaded yet.</p>';
        }
    } catch (err) {
        console.error("Failed to load files:", err);
    }
}

async function deleteFile(filename) {
    if (!confirm(`Are you sure you want to delete ${filename}?`)) return;

    try {
        const res = await fetch(`http://localhost:3000/api/files/${filename}`, {
            method: "DELETE"
        });
        const data = await res.json();
        if (data.message) {
            loadFiles();
        } else {
            alert("Error: " + data.error);
        }
    } catch (err) {
        console.error("Delete failed:", err);
    }
}

// Function to select a file and show it in preview (if it's an image)
function selectFile(filename) {
    // In a real app, you'd fetch the file URL from the server
    // For now, let's assume images are accessible via /user/uploads/filename
    // But since we are on local, we might need the full path or a proxy
    const img = document.querySelector(".logo-preview img");
    if (img && (filename.endsWith('.png') || filename.endsWith('.jpg') || filename.endsWith('.jpeg') || filename.endsWith('.svg'))) {
        // This won't work directly due to browser security (can't access local files)
        // But if the server serves them, we can use the URL.
        // For now, we'll just log it.
        console.log("Selected file:", filename);
    }
}

// MENU HOVER
document.addEventListener("DOMContentLoaded", () => {
    const items = document.querySelectorAll(".menu-item");

    items.forEach(item => {
        item.addEventListener("mouseenter", () => {
            items.forEach(i => i.classList.remove("active"));
            item.classList.add("active");
        });

        item.addEventListener("mouseleave", () => {
            item.classList.remove("active");
        });
    });

    // Load files on page load if we are on edit.html
    if (window.location.pathname.includes("edit.html")) {
        loadFiles();
    }
});
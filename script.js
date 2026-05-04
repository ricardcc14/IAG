async function generateLogo(brand_name, style, colors) {
    const res = await fetch("http://localhost:5000/api/logo", {
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
    const res = await fetch("http://localhost:5000/api/palette", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            brand_name: document.getElementById("name").value,
            style: "minimalist"
        })
    });
    const data = await res.json();
    const palette = JSON.parse(data.palette);
    // aquí depois asignas los colores a los divs visuales de tu HTML
    console.log(palette); // array de 5 hex codes
}





// MENU HOVER
const items = document.querySelectorAll(".menu-item");

items.forEach(item => {

    // Quan passes el ratolí per sobre d’un item
    item.addEventListener("mouseenter", () => {
        items.forEach(i => i.classList.remove("active"));
        item.classList.add("active");
    });

    // Quan el ratolí surt de l’item
    item.addEventListener("mouseleave", () => {
        item.classList.remove("active");
    });

});
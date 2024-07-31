document.addEventListener("DOMContentLoaded", function() {
    const titles = document.querySelectorAll(".project_title h3");
    titles.forEach(title => {
        if (title.textContent.length > 32) {
            title.textContent = title.textContent.substring(0, 32) + "...";
        }
    });
});
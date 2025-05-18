document.addEventListener("DOMContentLoaded", function () {
    const links = document.querySelectorAll(".left-navbar a");
    const underline = document.querySelector(".left-navbar .underline");
    const path = window.location.pathname;

    links.forEach(link => {
        if (link.getAttribute("href") === path) {
            const linkRect = link.getBoundingClientRect();
            const containerRect = link.parentElement.getBoundingClientRect();
            underline.style.width = `${link.offsetWidth}px`;
            underline.style.left = `${link.offsetLeft}px`;
        }

       
        link.addEventListener("mouseenter", () => {
            underline.style.width = `${link.offsetWidth}px`;
            underline.style.left = `${link.offsetLeft}px`;
        });
    });

   
    document.querySelector(".left-navbar").addEventListener("mouseleave", () => {
        const activeLink = Array.from(links).find(link => link.getAttribute("href") === path);
        if (activeLink) {
            underline.style.width = `${activeLink.offsetWidth}px`;
            underline.style.left = `${activeLink.offsetLeft}px`;
        }
    });
});

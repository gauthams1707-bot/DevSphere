
// DevSphere - Main JavaScript

document.addEventListener("DOMContentLoaded", function () {

    // 1. Dark / Light Theme Toggle
    const themeToggle = document.getElementById("themeToggle");

    const savedTheme = localStorage.getItem("devsphere-theme");

    if (savedTheme === "light") {
        document.body.classList.add("light-mode");

        if (themeToggle) {
            themeToggle.textContent = "🌙";
        }
    }

    if (themeToggle) {
        themeToggle.addEventListener("click", function () {
            document.body.classList.toggle("light-mode");

            const isLightMode = document.body.classList.contains("light-mode");

            localStorage.setItem(
                "devsphere-theme",
                isLightMode ? "light" : "dark"
            );

            themeToggle.textContent = isLightMode ? "🌙" : "☀";
        });
    }


    // 2. Mobile Navigation Menu
    const menuToggle = document.getElementById("menuToggle");
    const navLinks = document.getElementById("navLinks");

    if (menuToggle && navLinks) {
        menuToggle.addEventListener("click", function () {
            navLinks.classList.toggle("show");

            const isOpen = navLinks.classList.contains("show");

            menuToggle.textContent = isOpen ? "✕" : "☰";
            menuToggle.setAttribute(
                "aria-label",
                isOpen ? "Close menu" : "Open menu"
            );
        });

        // Close menu after selecting a navigation link
        navLinks.querySelectorAll("a").forEach(function (link) {
            link.addEventListener("click", function () {
                navLinks.classList.remove("show");
                menuToggle.textContent = "☰";
                menuToggle.setAttribute("aria-label", "Open menu");
            });
        });
    }


    // 3. Prevent accidental multiple form submissions
    document.querySelectorAll("form").forEach(function (form) {
        form.addEventListener("submit", function () {
            const submitButton = form.querySelector(
                'button[type="submit"]'
            );

            if (submitButton && form.checkValidity()) {
                submitButton.disabled = true;
                submitButton.style.opacity = "0.7";
                submitButton.textContent = "Please wait...";
            }
        });
    });


    // 4. Current year in footer
    document.querySelectorAll(".footer-bottom p").forEach(function (footer) {
        footer.textContent = footer.textContent.replace(
            /©\s*\d{4}/,
            "© " + new Date().getFullYear()
        );
    });

});

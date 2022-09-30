function navbarColorOnResize() { 
    sidenav && (1200 < window.innerWidth ? referenceButtons.classList.contains("active") && "bg-transparent" === referenceButtons.getAttribute("data-class") ? sidenav.classList.remove("bg-white") : document.querySelector("body").classList.contains("dark-version") || sidenav.classList.add("bg-white") : sidenav.classList.remove("bg-transparent"))
}
/* Script for theme switching */
const themeSwitch = document.getElementById('themeSwitch');
const currentTheme = localStorage.getItem("theme");

if (currentTheme) {
    document.documentElement.setAttribute("data-theme", currentTheme);
}

themeSwitch.onclick = () => {
    if (document.documentElement.getAttribute('data-theme') === 'light') {
        document.documentElement.setAttribute('data-theme', 'dark');
        localStorage.setItem("theme", "dark");
    } else {
        document.documentElement.setAttribute('data-theme', 'light');
        localStorage.setItem("theme", "light");
    }
}

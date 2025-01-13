function Darkmode() {
  var element = document.body;
  console.log("Dark mode toggle clicked");
  element.classList.toggle("dark-mode");
  if (element.classList.contains("dark-mode")) {
      localStorage.setItem("theme", "dark");
  } else {
      localStorage.setItem("theme", "light");
  }
}

function loadTheme() {
  const theme = localStorage.getItem("theme");
  if (theme) {
      document.body.classList.toggle("dark-mode", theme === "dark");
  }
}

window.onload = loadTheme;function Darkmode() {
  var element = document.body;
  console.log("Dark mode toggle clicked");
  element.classList.toggle("dark-mode");
  if (element.classList.contains("dark-mode")) {
      localStorage.setItem("theme", "dark");
  } else {
      localStorage.setItem("theme", "light");
  }
}

function loadTheme() {
  const theme = localStorage.getItem("theme");
  if (theme) {
      document.body.classList.toggle("dark-mode", theme === "dark");
  }
}

window.onload = loadTheme;
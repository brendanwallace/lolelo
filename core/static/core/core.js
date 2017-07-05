document.getElementById("standings-select").onclick = function() {
    document.getElementById("standings").classList.remove("display-none");
    document.getElementById("upcoming").classList.add("display-none");
    document.getElementById("standings-select").classList.add("selected");
    document.getElementById("upcoming-select").classList.remove("selected");
};

document.getElementById("upcoming-select").onclick = function() {
    document.getElementById("upcoming").classList.remove("display-none");
    document.getElementById("standings").classList.add("display-none");
    document.getElementById("upcoming-select").classList.add("selected");
    document.getElementById("standings-select").classList.remove("selected");
};

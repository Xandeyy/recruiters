// Function to toggle the dropdown menu
function toggleDropdown() {
  var dropdownMenu = document.getElementById("dropdown-menu");
  dropdownMenu.classList.toggle("hidden");
}

// Close the dropdown if clicked outside of it
window.onclick = function (event) {
  if (
    !event.target.matches(".dropdown-button") &&
    !event.target.closest(".dropdown-button")
  ) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    for (var i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (!openDropdown.classList.contains("hidden")) {
        openDropdown.classList.add("hidden");
      }
    }
  }
};

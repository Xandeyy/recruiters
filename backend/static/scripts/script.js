// Function to toggle the dropdown menu
function toggleDropdown() {
  var dropdownMenu = document.getElementById("dropdown-menu");
  dropdownMenu.classList.toggle("hidden");
}

// Function to toggle the company dropdown menu
function toggleCompanyDropdown() {
  var companyDropdownMenu = document.getElementById("company-dropdown-menu");
  companyDropdownMenu.classList.toggle("hidden");
}

// Close the dropdowns if clicked outside of them
window.onclick = function (event) {
  if (
    !event.target.matches(".dropdown-button") &&
    !event.target.closest(".dropdown-button")
  ) {
    var dropdowns = document.querySelectorAll(".dropdown-content");
    dropdowns.forEach(function (dropdown) {
      if (!dropdown.classList.contains("hidden")) {
        dropdown.classList.add("hidden");
      }
    });
  }
};

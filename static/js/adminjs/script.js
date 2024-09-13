document.addEventListener('DOMContentLoaded', function() {
  const searchInput = document.getElementById('doctor-search');
  const tableRows = document.querySelectorAll('.doctors-table tbody tr');
  const noResults = document.getElementById('no-results');

  searchInput.addEventListener('input', function() {
      const filter = searchInput.value.toLowerCase();
      let found = false;

      tableRows.forEach(function(row) {
          const departmentName = row.getAttribute('data-name').toLowerCase();
          if (departmentName.includes(filter)) {
              row.style.display = 'table-row';
              found = true;
          } else {
              row.style.display = 'none';
          }
      });

      noResults.style.display = found ? 'none' : 'block';
  });
});


document.addEventListener('DOMContentLoaded', function() {
  const searchInput = document.getElementById('department-search');
  const tableRows = document.querySelectorAll('.departments-table tbody tr');
  const noResults = document.getElementById('no-results');

  searchInput.addEventListener('input', function() {
      const filter = searchInput.value.toLowerCase();
      let found = false;

      tableRows.forEach(function(row) {
          const departmentName = row.getAttribute('data-name').toLowerCase();
          if (departmentName.includes(filter)) {
              row.style.display = 'table-row';
              found = true;
          } else {
              row.style.display = 'none';
          }
      });

      noResults.style.display = found ? 'none' : 'block';
  });
});


document.addEventListener('DOMContentLoaded', () => {
  const dropdownToggles = document.querySelectorAll('.dropdown-toggle');

  dropdownToggles.forEach(toggle => {
      toggle.addEventListener('click', (e) => {
          e.preventDefault(); // Prevent default anchor behavior
          const parentDropdown = toggle.parentElement; // Get the parent dropdown element
          const dropdownMenu = parentDropdown.querySelector('.dropdown-menu'); // Get the associated dropdown menu

          // Close any open dropdowns
          document.querySelectorAll('.dropdown-menu').forEach(menu => {
              if (menu !== dropdownMenu) {
                  menu.parentElement.classList.remove('open');
              }
          });

          // Toggle the clicked dropdown menu
          parentDropdown.classList.toggle('open');
      });
  });

  // Close dropdowns when clicking outside of them
  document.addEventListener('click', (e) => {
      if (!e.target.closest('.dropdown')) {
          document.querySelectorAll('.dropdown-menu').forEach(menu => {
              menu.parentElement.classList.remove('open');
          });
      }
  });
});


document.addEventListener("DOMContentLoaded", function() {
    const monthPicker = document.getElementById("month-picker");
    const tableRows = document.querySelectorAll(".appointments-table tbody tr");
  
    function filterAppointments(selectedMonth) {
      let found = false;
      const [year, month] = selectedMonth.split('-').map(Number);
  
      tableRows.forEach(function(row) {
        const dateCell = row.querySelector("td:nth-child(2)");
        if (dateCell) {
          const dateText = dateCell.textContent;
          const appointmentDate = new Date(dateText);
  
          // Extract year and month from the appointment date
          const appointmentYear = appointmentDate.getFullYear();
          const appointmentMonth = appointmentDate.getMonth() + 1; // Months are zero-based
  
          if (appointmentYear === year && appointmentMonth === month) {
            row.style.display = "";
            found = true;
          } else {
            row.style.display = "none";
          }
        }
      });
  
      // Show a "No appointments found" message if no rows match
      const noMatchRow = document.querySelector(".no-match");
      if (!found) {
        if (!noMatchRow) {
          const newRow = document.createElement("tr");
          newRow.classList.add("no-match");
          newRow.innerHTML = `<td colspan="7" style="text-align: center;">No appointments found</td>`;
          document.querySelector(".appointments-table tbody").appendChild(newRow);
        }
      } else {
        if (noMatchRow) {
          noMatchRow.remove();
        }
      }
    }
  
    // Set the default value to the current month
    const today = new Date();
    const currentMonth = today.toISOString().slice(0, 7); // Format as YYYY-MM
    monthPicker.value = currentMonth;
    filterAppointments(currentMonth);
  
    monthPicker.addEventListener("change", function() {
      filterAppointments(monthPicker.value);
    });
  });
  
  document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('department-search');
    const tableBody = document.getElementById('department-table-body');
    const rows = tableBody.getElementsByTagName('tr');

    searchInput.addEventListener('keyup', function() {
        const searchTerm = searchInput.value.toLowerCase();

        Array.from(rows).forEach(function(row) {
            const departmentName = row.getAttribute('data-name').toLowerCase();
            
            if (departmentName.includes(searchTerm)) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    });
});

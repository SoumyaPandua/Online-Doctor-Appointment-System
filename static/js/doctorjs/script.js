document.querySelectorAll('.dropdown-toggle').forEach(toggle => {
  toggle.addEventListener('click', function(event) {
      event.preventDefault();
      const dropdown = this.parentElement;
      dropdown.classList.toggle('open');
  });
});

document.addEventListener("DOMContentLoaded", function() {
  const searchInput = document.querySelector(".search");
  const tableRows = document.querySelectorAll(".appointments-table tbody tr");

  searchInput.addEventListener("keyup", function() {
      const filter = searchInput.value.toLowerCase();
      let found = false;

      tableRows.forEach(function(row) {
          const cells = row.querySelectorAll("td");
          let match = false;

          cells.forEach(function(cell, index) {
              // Check the columns: APT. NO. (index 0), APT. DATE (index 1), PATIENT NAME (index 2), EMAIL (index 3), PHONE (index 4)
              if (index <= 4 && cell.textContent.toLowerCase().includes(filter)) {
                  match = true;
              }
          });

          if (match) {
              row.style.display = "";
              found = true;
          } else {
              row.style.display = "none";
          }
      });

      // If no rows match the search, show a "No appointments found" message
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
  });
});

document.addEventListener('DOMContentLoaded', function() {
  // Get the current date
  const today = new Date();

  // Get the month name
  const monthNames = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
  ];
  const month = monthNames[today.getMonth()];

  // Get the day and year
  const day = today.getDate();
  const year = today.getFullYear();

  // Construct the date string
  const dateString = `${month} ${day}, ${year}`;

  // Set the date string in the header
  const dateElement = document.querySelector('.main-content header .date');
  if (dateElement) {
    dateElement.textContent = dateString;
  }
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

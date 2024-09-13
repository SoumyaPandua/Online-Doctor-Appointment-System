document.querySelector(".hamburger").addEventListener("click", () => {
  document.querySelector(".nav-links").classList.toggle("active");
});

document.addEventListener("DOMContentLoaded", function () {
  const departments = document.querySelectorAll('.department');
  const searchInput = document.getElementById('department-search');
  const noResults = document.getElementById('no-results');

  // Search Functionality
  searchInput.addEventListener('input', function () {
      const filter = searchInput.value.toLowerCase();
      let found = false;

      departments.forEach(function (department) {
          const departmentName = department.getAttribute('data-name');
          if (departmentName.includes(filter)) {
              department.style.display = 'block';
              found = true;
          } else {
              department.style.display = 'none';
          }
      });

      noResults.style.display = found ? 'none' : 'block';
  });
});

document.getElementById('doctor-search').addEventListener('input', function() {
  const searchValue = this.value.toLowerCase();
  const doctorCards = document.querySelectorAll('.doctor-card');
  let doctorFound = false;

  doctorCards.forEach(function(card) {
      const doctorName = card.querySelector('h3').textContent.toLowerCase();
      if (doctorName.includes(searchValue)) {
          card.style.display = 'block';
          doctorFound = true;
      } else {
          card.style.display = 'none';
      }
  });

  if (!doctorFound) {
      document.getElementById('no-doctor-results').style.display = 'block';
  } else {
      document.getElementById('no-doctor-results').style.display = 'none';
  }
});

document.getElementById('reset-search').addEventListener('click', function() {
  document.getElementById('doctor-search').value = '';
  document.getElementById('no-doctor-results').style.display = 'none';

  const doctorCards = document.querySelectorAll('.doctor-card');
  doctorCards.forEach(function(card) {
      card.style.display = 'block';
  });
});



// JavaScript for FAQ section

// Function to search FAQs
function searchFAQs() {
    const input = document.getElementById('faq-search').value.toLowerCase();
    const faqItems = document.querySelectorAll('.faq-item');
    let hasResults = false;
  
    faqItems.forEach(item => {
      const question = item.querySelector('.faq-question span').innerText.toLowerCase();
      const answer = item.querySelector('.faq-answer').innerText.toLowerCase();
  
      if (question.includes(input) || answer.includes(input)) {
        item.style.display = '';
        hasResults = true;
      } else {
        item.style.display = 'none';
      }
    });
  
    // Show "No Results" message if no items match the search
    document.querySelector('.no-results').style.display = hasResults ? 'none' : 'block';
  }
  
  // Function to toggle FAQ answer visibility
  function toggleFAQ(element) {
    const answer = element.nextElementSibling;
    const icon = element.querySelector('i');
  
    if (answer.classList.contains('open')) {
      answer.classList.remove('open');
      icon.classList.replace('fa-minus', 'fa-plus');
    } else {
      answer.classList.add('open');
      icon.classList.replace('fa-plus', 'fa-minus');
    }
  }
  
  // Attach event listeners to all FAQ items
  document.querySelectorAll('.faq-question').forEach(question => {
    question.addEventListener('click', function() {
      toggleFAQ(this);
    });
  });
  
// JavaScript to handle the star rating interaction
const stars = document.querySelectorAll('.star-rating i');
const ratingInput = document.getElementById('rating');

stars.forEach(star => {
  star.addEventListener('click', () => {
    const ratingValue = star.getAttribute('data-value');
    ratingInput.value = ratingValue;

    stars.forEach((s, index) => {
      if (index < ratingValue) {
        s.style.color = '#ffdd00';
      } else {
        s.style.color = '#ccc';
      }
    });
  });
});
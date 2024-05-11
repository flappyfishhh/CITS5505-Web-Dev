document.addEventListener('DOMContentLoaded', function() {
    var searchInput = document.getElementById('search');
    var searchIcon = document.querySelector('.swap-on');
    var closeButton = document.querySelector('.close-btn');
  
    searchIcon.addEventListener('click', function() {
        performSearch(searchInput.value);
    });
  
    searchInput.addEventListener('input', function(event) {
        event.preventDefault();
        performSearch(searchInput.value);
    });
  
    closeButton.addEventListener('click', function() {
        searchInput.value = '';
    });
  
    function performSearch(query) {
      fetch('/search', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({ query: query })
      })
      .then(response => {
          if (!response.ok) {
              throw new Error('Network response was not ok');
          }
          return response.text();
      })
      .then(response => {
        document.querySelector(".content-container").innerHTML = response
      })
      .catch(error => {
          console.error('There has been a problem with your fetch operation:', error);
      });
    }
  
    
  });
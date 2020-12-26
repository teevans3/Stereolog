// Variables for search-album popup and search results popup (if it exists)
var searchAlbumForm = document.getElementById('searchAlbumForm');
var searchResults = document.querySelector('.search-results-popup');

// Function for opening/closing popups
document.getElementById('displaySearch').addEventListener("click", function() {
  // If search album popup, hide it; if search results, remove them
  if (searchAlbumForm.classList.contains('show-popup')) {
    searchAlbumForm.classList.toggle('show-popup');
  };
  if (searchResults) {
    searchResults.remove();
  };
  searchAlbumForm.classList.toggle('show-popup');
});

// Function for closing popups via close buttons
var popupClosers = document.querySelectorAll('.close-popup');
popupClosers.forEach(function(item) {
  item.addEventListener('click', function() {
    // If search album popup, hide it; if search results, remove them
    if (searchAlbumForm.classList.contains('show-popup')) {
      searchAlbumForm.classList.toggle('show-popup');
    };
    if (searchResults) {
      searchResults.remove();
    };
  });
});

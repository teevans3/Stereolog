// Variables for add-album form, search results popup (if it exists), and delete-list form
var addAlbumForm = document.getElementById('addAlbumForm');
var searchResults = document.querySelector('.search-results-popup');
var deleteListForm = document.getElementById('deleteListForm');
// Array of all "close" buttons for exiting popups
var popupClosers = document.querySelectorAll('.close-popup');

// Function for displaying the add-album form
document.getElementById('displaySearchList').addEventListener("click", function() {
  // If search results, remove them; if delete-list popup, hide it
  if (searchResults) {
    searchResults.remove();
  };
  if (deleteListForm.classList.contains('show-popup')) {
    deleteListForm.classList.toggle('show-popup');
  };
  addAlbumForm.classList.toggle('show-popup');
});

// Function for displaying the delete-list form
document.getElementById('displayDeleteList').addEventListener('click', function() {
  // If search results, remove them; if sadd-album popup, hide it
  if (searchResults) {
    searchResults.remove();
  };
  if (addAlbumForm.classList.contains('show-popup')) {
    addAlbumForm.classList.toggle('show-popup');
  };
  deleteListForm.classList.toggle('show-popup');
});

// Function for closing popups via close buttons
popupClosers.forEach(function(item) {
  item.addEventListener('click', function() {
    // If add-album popup or delete-list popup, hide them; if search results, remove them
    if (addAlbumForm.classList.contains('show-popup')) {
      addAlbumForm.classList.toggle('show-popup');
    };
    if (deleteListForm.classList.contains('show-popup')) {
      deleteListForm.classList.toggle('show-popup');
    }
    if (searchResults) {
      searchResults.remove();
    };
  });
});

// Functions for checking if the album already exists in the user's lists
var addAlbumBtns = document.querySelectorAll('.addAlbumBtn');
addAlbumBtns.forEach(function(btn) {
  btn.addEventListener('click', function(event) {
    event.preventDefault();
    // Send the album_id and list title to server to see if album exists in the list already
    var albumId = btn.value;
    var listTitle = document.getElementById('listTitle').innerHTML;
    $.get('/accounts/check_album_in_list', {"album_id": albumId, "list_title": listTitle}, function(data) {
        if (data.duplicate == true) {
          alert("This album is already in your list.");
        } else {
          document.forms[albumId].submit();
        };
    });
  });
});

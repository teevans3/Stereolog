// Variables for edit-review- and delete-review-forms
var editForm = document.getElementById('editForm');
var deleteForm = document.getElementById('deleteForm');

// Functions for opening/closing both edit-review and delete-review-forms (popups)
document.getElementById('displayEdit').addEventListener("click", function() {
    // Hide the edit-review-form if displayed
    if (deleteForm.classList.contains('show-popup') == true) {
      deleteForm.classList.toggle('show-popup');
    };
    editForm.classList.toggle('show-popup');
});
document.getElementById('displayDelete').addEventListener("click", function() {
    // Hide the edit-review-form if displayed
    if (editForm.classList.contains('show-popup') == true) {
      editForm.classList.toggle('show-popup');
    };
    deleteForm.classList.toggle('show-popup');
});

// Function for submitting the user's edited review, checking if all the fields are filled out
document.getElementById('submitEdit').addEventListener("click", function(event) {
  event.preventDefault();
  if (document.forms['editForm']['rating'].value == "") {
    alert("Please offer a rating.");
  } else {
    if (document.forms['editForm']['like'].value == "") {
      alert("Did you like the album?");
    } else {
      if (document.forms['editForm']['review'].value == "") {
        alert("Please write a review");
      } else {
        alert("Review successfully edited!");
        document.forms['editForm'].submit();
      };
    };
  };
});

// Function for closing popups via close buttons
var popupClosers = document.querySelectorAll('.close-popup');
popupClosers.forEach(function(item) {
  item.addEventListener('click', function() {
    if (editForm.classList.contains('show-popup')) {
      editForm.classList.toggle('show-popup');
    };
    if (deleteForm.classList.contains('show-popup')) {
      deleteForm.classList.toggle('show-popup');
    };
  });
});

// Functions for changing the style of thumbs up/down icons when they are clicked
document.getElementById('yes').addEventListener('click', function() {
  // If the thumbs-down active first, revert to old style
  if (document.querySelector('.form-thumbs-down').classList.contains('form-thumbs-active')) {
    document.querySelector('.form-thumbs-down').classList.toggle('form-thumbs-active');
  };
  document.querySelector('.form-thumbs-up').classList.toggle('form-thumbs-active');
});
document.getElementById('no').addEventListener('click', function() {
  // If the thumbs-up active first, revert to old style
  if (document.querySelector('.form-thumbs-up').classList.contains('form-thumbs-active')) {
    document.querySelector('.form-thumbs-up').classList.toggle('form-thumbs-active');
  };
  document.querySelector('.form-thumbs-down').classList.toggle('form-thumbs-active');
})

// Functions for opening/closing create-list form (popup)
document.getElementById('displayCreate').addEventListener("click", function() {
    // Display/hide the popup edit-review-form
    document.getElementById('createForm').classList.toggle('show-popup');
});

// Function for closing popups (via close button)
document.querySelector('.close-popup').addEventListener("click", function() {
  document.getElementById('createForm').classList.toggle('show-popup');
});

// Function for creating a new list
document.getElementById('createList').addEventListener("click", function(event) {
  event.preventDefault();
  // Ensure all of the fields are filled out and check if user has a list with the same title
  if (document.forms['createForm']['list_title'].value == "") {
    alert("Add a title");
  } else {
    if (document.forms['createForm']['list_description'].value == "") {
      alert("Add a description");
    } else {
      $.get('/lists/check_list_title', {'new_list_title': document.forms['createForm']['list_title'].value}, function(data) {
          if (data.unique_title == false) {
            alert("You already have a list with this title!");
          } else {
            alert("List successfully created!");
            document.forms['createForm'].submit();
          };
      });
    };
  };
});

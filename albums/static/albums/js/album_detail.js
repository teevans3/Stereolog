// Functions for opening/closing popups
document.getElementById('displayReview').addEventListener("click", function() {
  // Ensure the user has not already submitted a review
  allReviews = document.querySelectorAll('.review-short');
  if (allReviews.length > 0) {
    for (i = 0; i < allReviews.length; i++) {
      // Compare all review author names with username signed in
      var reviewAuthor = allReviews[i].querySelector('.review-author').innerHTML;
      var sessionUser = document.querySelector('#sessionUser').innerHTML;
      if (reviewAuthor === sessionUser) {
        // If user has already written a review, redirect them to their review page (where they can choose to edit it)
        alert("You have already written a review for this!");
        var albumID = document.forms['reviewForm']['album_id'].value;
        window.location.href = `/accounts/${sessionUser}/reviews/${albumID}`;
        return;
      };
    };
    // Otherwise, display the popup form for the review
    document.getElementById('reviewForm').classList.toggle('show-popup');
  } else {
    document.getElementById('reviewForm').classList.toggle('show-popup');
  };
});

// Function for submitting the user's review, checking if all the fields are filled out
document.getElementById('submitReview').addEventListener("click", function(event) {
  event.preventDefault();
  if (document.forms['reviewForm']['rating'].value == "") {
    alert("Please offer a rating.");
  } else {
    if (document.forms['reviewForm']['like'].value == "") {
      alert("Did you like the album?");
    } else {
      if (document.forms['reviewForm']['review'].value == "") {
        alert("Please write a review");
      } else {
        alert("Review created!")
        document.forms['reviewForm'].submit();
      };
    };
  };
});

// Function for closing popups via close button
document.querySelector('.close-popup').addEventListener('click', function() {
    document.getElementById('reviewForm').classList.toggle('show-popup');
});

// Functions for changing the style of thumbs up/down icons when they are clicked
document.getElementById('yes').addEventListener('click', function() {
  // If the thumbs-down active first, revert to old style
  if (document.getElementById('thumbs-down-icon').classList.contains('form-thumbs-active')) {
    document.getElementById('thumbs-down-icon').classList.toggle('form-thumbs-active');
  };
  document.getElementById('thumbs-up-icon').classList.toggle('form-thumbs-active');
});
document.getElementById('no').addEventListener('click', function() {
  // If the thumbs-up active first, revert to old style
  if (document.getElementById('thumbs-up-icon').classList.contains('form-thumbs-active')) {
    document.getElementById('thumbs-up-icon').classList.toggle('form-thumbs-active');
  };
  document.getElementById('thumbs-down-icon').classList.toggle('form-thumbs-active');
})

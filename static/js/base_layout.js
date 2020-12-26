// Functions for checking if user has existing reviews, lists, and liked albums (for the subnav links)
document.getElementById('subnavReviews').addEventListener('click', function(event) {
  event.preventDefault();
  $.get('/accounts/check_user_info', {"info_type": "reviews"}, function(data) {
      // If user has no existing reviews, don't let them click the link; redirect to albums page
      if (data.has_reviews == false) {
        alert("You currently have no reviews.");
      } else {
        window.location.href = document.getElementById("subnavReviews").href;
      };
  });
});
document.getElementById('subnavLists').addEventListener('click', function(event) {
  event.preventDefault();
  $.get('/accounts/check_user_info', {"info_type": "lists"}, function(data) {
      // If user has no existing reviews, don't let them click the link; redirect to albums page
      if (data.has_lists == false) {
        alert("You currently have no lists.");
      } else {
        window.location.href = document.getElementById("subnavLists").href;
      };
  });
});
document.getElementById('subnavLikes').addEventListener('click', function(event) {
  event.preventDefault();
  $.get('/accounts/check_user_info', {"info_type": "likes"}, function(data) {
      // If user has no existing reviews, don't let them click the link; redirect to albums page
      if (data.has_likes == false) {
        alert("You currently have no likes.");
      } else {
        window.location.href = document.getElementById("subnavLikes").href;
      };
  });
});

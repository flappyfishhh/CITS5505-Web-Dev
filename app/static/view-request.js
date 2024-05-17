$(document).ready(function () {
  // Hide the response content initially
  $(".response-content").hide();

  // On clicking respond button, the response content section will be displayed
  $(".respond-button").click(function () {
    $(".respond-button").hide();
    $(".response-content").show();
    $(".response-content .back-button").show();
  });

  // On clicking back button, user can go back to view request page and response content section will be hidden
  $(".back-button").click(function () {
    $(".respond-button").show();
    $(".response-content").hide();
  });

  // Validate and submit the form
  $("form").submit(function () {
    const response = $("#response").val().trim();
    if (response === "") {
      alert("Please enter a response.");
      $("#response").focus(); // Focus on the response field
      return false; // Prevent form submission
    }
    // If response is not empty, allow form submission
    return true;
  });

  //using AJAX for displaying tags
  $(document).ready(function () {
    $(".tag-link").click(function (event) {
      event.preventDefault();
      var tag = $(this).html().substring(1); // Remove the '#' from the tag name
      fetch("/tag_requests/" + tag)
        .then((response) => response.text())
        .then((data) => {
          document.open();
          document.write(data);
          document.close();
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    });
  });
});


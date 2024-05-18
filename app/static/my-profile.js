$(document).ready(function () {
  // Get all elements with the class "collapsible"
  var coll = document.getElementsByClassName("collapsible");
  var i;

  // Loop through each collapsible element and add a click event listener
  for (i = 0; i < coll.length; i++) {
    coll[i].addEventListener("click", function () {
      this.classList.toggle("active");
      var content = this.nextElementSibling;
      if (content.style.display === "block") {
        content.style.display = "none";
      } else {
        content.style.display = "block";
      }
    });
  }

  // Add a click event listener to the element with the id 'avatar_file_show'
  document
    .getElementById("avatar_file_show")
    .addEventListener("click", function () {
      document.getElementById("avatar_file").click();
    });

  // Add a change event listener to the file input element
  document
    .getElementById("avatar_file")
    .addEventListener("change", function () {
      document.getElementById("avatar_file_show").text = "selected";
    });

  // Add a click event listener to the button with the id 'changeButton'
  document
    .getElementById("changeButton")
    .addEventListener("click", function (event) {
      var password_old = document.getElementById("password_old").value;
      var password_new = document.getElementById("password_new").value;
      var password_repeat = document.getElementById(
        "password_new_repeat"
      ).value;
      if (password_new !== password_repeat) {
        alert("The new password entered is inconsistent.");
      }
      var data = {
        password_old: password_old,
        password_new: password_new,
      };

      // Make an AJAX POST request to update the password
      $.ajax({
        type: "POST",
        url: "/update_password",
        data: JSON.stringify(data),
        contentType: "application/json",
        success: function (response) {
          // console.log(response.code)
          if (response.code == 0) {
            $(".changePassword_msg").text("Password changed!");
            $(".changePassword_msg").css("color", "green");
          } else {
            $(".changePassword_msg").text("Incorrect password!");
            $(".changePassword_msg").css("color", "red");
          }
        },
        error: function (xhr, status, error) {
          alert("Network Error");
        },
      });

      event.preventDefault(); // Prevent form submission
    });
});

// Get the form element and the result div
var form = document.querySelector("form");
var resultDiv = document.querySelector("#result"); // Changed the name to resultDiv

// Define a function to handle the form submission
function handleSubmit(event) {
  // Prevent the default behavior of reloading the page
  event.preventDefault();

  // Get the file input element and the selected file
  var fileInput = document.querySelector("#image");
  var file = fileInput.files[0];

  // Check if a file is selected
  if (file) {
    // Create a FormData object and append the file
    var formData = new FormData();
    formData.append("image", file);

    // Create an XMLHttpRequest object and set the response type to JSON
    var xhr = new XMLHttpRequest();
    xhr.responseType = "json";

    // Define a function to handle the response
    xhr.onload = function() {
      // Check if the status is OK
      if (xhr.status === 200) {
        // Get the response data
        var data = xhr.response;

        // Check if there are any results
        if (data.results && data.results.length > 0) {
          // Get the first result and its plate number
          var firstResult = data.results[0]; // Changed the name to firstResult
          var plate = firstResult.plate;

          // Display the plate number in the result div
          resultDiv.innerHTML = "Plate number: " + plate; // Changed result to resultDiv
        } else {
          // Display an error message in the result div
          resultDiv.innerHTML = "No plates detected."; // Changed result to resultDiv
        }
      } else {
        // Display an error message in the result div
        resultDiv.innerHTML = "An error occurred: " + xhr.statusText; // Changed result to resultDiv
      }
    };

    // Define a function to handle the error
    xhr.onerror = function() {
      // Display an error message in the result div
      resultDiv.innerHTML = "An error occurred: " + xhr.statusText; // Changed result to resultDiv
    };

    // Open a POST request to the upload endpoint
    xhr.open("POST", "/result/");

    // Send the FormData object
    xhr.send(formData);
  } else {
    // Display an error message in the result div
    resultDiv.innerHTML = "Please select an image file."; // Changed result to resultDiv
  }
}

// Add an event listener to the form submission
form.addEventListener("submit", handleSubmit);
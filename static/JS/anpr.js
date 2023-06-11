// Get the form element and the result div
var form = document.querySelector("form");
var resultDiv = document.querySelector("#result"); // Changed the name to resultDiv
const csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value;

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
const csrftoken = getCookie('csrftoken');

// Define a function to handle the form submission
function handleSubmit(event) {
  // Prevent the default behavior of reloading the page
  event.preventDefault();

  // Get the file input element and the selected file
  var fileInput = document.querySelector("#image");
  var file = fileInput.files[0];
  // var csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
  // Check if a file is selected
  if (file) {
    // Create a FormData object and append the file
    var formData = new FormData();
    formData.append("image", file);

    // Create an XMLHttpRequest object and set the response type to JSON
    var xhr = new XMLHttpRequest();
    xhr.responseType = "json";

    // Define a function to handle the response
    xhr.onload = function () {
      // Check if the status is OK
      if (xhr.status === 200) {
        // Get the response data
        var data = xhr.response;
        console.log(data.img)
        // Check if there are any results
        if (data.length !== 0) {
          // Get the first result and its plate number
          var firstResult = data.ocr_output; // Changed the name to firstResult
          var plate = data.img;
          // Display the plate number in the result div
          resultDiv.innerHTML = "Plate number: " + firstResult;
          var img = document.createElement("img");
          img.src = plate;
          resultDiv.appendChild(img); // Changed result to resultDiv
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
    xhr.onerror = function () {
      // Display an error message in the result div
      resultDiv.innerHTML = "An error occurred: " + xhr.statusText; // Changed result to resultDiv
    };
    // Open a POST request to the upload endpoint
    // import csrf_token from django.middleware.csrf import get_token
    // js cookie module to get csrf token from cookie 
    // var csrf_token = get_token(request)

    
    console.log(csrf_token)
    xhr.open("POST", "/result/");
    xhr.setRequestHeader("X-CSRFToken", csrf_token);
    // Send the FormData object
    xhr.send(formData);
  } else {
    // Display an error message in the result div
    resultDiv.innerHTML = "Please select an image file."; // Changed result to resultDiv
  }
}

// Add an event listener to the form submission
form.addEventListener("submit", handleSubmit);
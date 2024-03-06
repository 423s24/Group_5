document.getElementById('delete-button').addEventListener('click', function(event) {
    var confirmed = window.confirm('Are you sure you want to delete this account?');
    if (!confirmed) {
        // Prevent the default link action (following the link)
        event.preventDefault();
    }
});

document.getElementById('cancel-button').addEventListener('click', function() {
    location.reload();
});

document.getElementById('edit-button').addEventListener('click', function() {
  // Hide profile info, show edit form
  document.getElementById('profile-info').style.display = 'none';
  document.getElementById('edit-form').style.display = 'block';
  
  // Populate edit fields with current info
  document.getElementById('edit-first-name').value = document.getElementById('first-name').innerText;
  document.getElementById('edit-last-name').value = document.getElementById('last-name').innerText;
  document.getElementById('edit-username').value = document.getElementById('username').innerText;
  document.getElementById('edit-email').value = document.getElementById('email').innerText;
});

document.getElementById('save-button').addEventListener('click', function() {
  // Update profile info with edited values
  document.getElementById('first-name').innerText = document.getElementById('edit-first-name').value;
  document.getElementById('last-name').innerText = document.getElementById('edit-last-name').value;
  document.getElementById('username').innerText = document.getElementById('edit-username').value;
  document.getElementById('email').innerText = document.getElementById('edit-email').value;
  
  // Hide edit form, show profile info
  submitProfileChanges();
  document.getElementById('edit-form').style.display = 'none';
  document.getElementById('profile-info').style.display = 'block';
});

// Function to submit profile changes
function submitProfileChanges() {
    // Gather updated profile information from form fields
    var updatedProfileData = {
        first_name: document.getElementById('edit-first-name').value,
        last_name: document.getElementById('edit-last-name').value,
        username: document.getElementById('edit-username').value,
        email: document.getElementById('edit-email').value,
        // Add other fields as needed
    };

    // Send a POST request to the Django /user URL
    fetch(window.location.pathname, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Get CSRF token from cookie
        },
        credentials: 'same-origin', // Include cookies in the request
        body: JSON.stringify(updatedProfileData) // Convert data to JSON format
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        // Handle successful response
        console.log('Profile changes submitted successfully');
    })
    .catch(error => {
        // Handle errors
        console.error('Error submitting profile changes:', error);
    });
}

// Function to get CSRF token from cookie
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Check if the cookie name matches the desired name
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
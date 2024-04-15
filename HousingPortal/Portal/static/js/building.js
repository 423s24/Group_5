document.getElementById('cancel-button').addEventListener('click', function() {
    document.getElementById('edit-form').style.display = 'none';
    document.getElementById('building-info').style.display = 'block';
});

document.getElementById('edit-button').addEventListener('click', function() {
    // Hide profile info, show edit form
    document.getElementById('building-info').style.display = 'none';
    document.getElementById('edit-form').style.display = 'block';
    
    // Populate edit fields with current info
    document.getElementById('edit-building-name').value = document.getElementById('building-name').innerText;
    document.getElementById('edit-building-address').value = document.getElementById('building-address').innerText;
    document.getElementById('edit-building-city').value = document.getElementById('building-city').innerText;
    document.getElementById('edit-building-state').value = document.getElementById('building-state').innerText;
    document.getElementById('edit-building-country').value = document.getElementById('building-country').innerText;
    document.getElementById('edit-building-zipcode').value = document.getElementById('building-zipcode').innerText;
});

document.getElementById('save-button').addEventListener('click', function() {
    // Update profile info with edited values
    document.getElementById('building-name').innerText = document.getElementById('edit-building-name').value;
    document.getElementById('building-address').innerText = document.getElementById('edit-building-address').value;
    document.getElementById('building-city').innerText = document.getElementById('edit-building-city').value;
    document.getElementById('building-state').innerText = document.getElementById('edit-building-state').value;
    document.getElementById('building-country').innerText = document.getElementById('edit-building-country').value;
    document.getElementById('building-zipcode').innerText = document.getElementById('edit-building-zipcode').value;
    
    // Hide edit form, show profile info
    submitChanges();
    document.getElementById('edit-form').style.display = 'none';
    document.getElementById('building-info').style.display = 'block';
});

function submitChanges() {
    var updatedProfileData = {
        name: document.getElementById('edit-building-name').value,
        address: document.getElementById('edit-building-address').value,
        city: document.getElementById('edit-building-city').value,
        state: document.getElementById('edit-building-state').value,
        country: document.getElementById('edit-building-country').value,
        zipcode: document.getElementById('edit-building-zipcode').value,
    };

    fetch(window.location.origin + window.location.pathname, {
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
        console.log('Changes submitted successfully');
    })
    .catch(error => {
        // Handle errors
        console.error('Error submitting changes:', error);
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
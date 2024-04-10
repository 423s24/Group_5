document.addEventListener("DOMContentLoaded", function() {
    var usernameInput = document.getElementById("id_username");

    async function checkUsername() {
        var username = usernameInput.value.trim(); // Trim whitespace from the input
        
        try {
            // Make an asynchronous request to check if the username exists
            var usernameExists = await check_username(username);
    
            // Change style of username input field based on whether the username exists
            if (usernameExists) {
                usernameInput.style.borderColor = "red";
            } else {
                usernameInput.style.borderColor = ""; // Reset to default
            }
        } catch (error) {
            console.error('Error checking username:', error);
            // Handle error here if needed
        }
    }
    
    usernameInput.addEventListener("input", checkUsername);    
});

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

async function check_username(username) {
    try {
        const response = await fetch('/check_username/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') // Get CSRF token from cookie
            },
            credentials: 'same-origin', // Include cookies in the request
            body: JSON.stringify({ username: username })
        });
        
        const data = await response.json();

        // Check if 'taken' key exists in the response
        if ('taken' in data) {
            return data.taken;
        } else {
            return false;
        }
    } catch (error) {
        console.error('Error checking username:', error);
        throw error; // Re-throw the error to propagate it further
    }
}

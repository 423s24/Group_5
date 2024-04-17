window.onload = function() {
    var deleteUserModal = document.getElementById("deleteUserModal");
    var confirmDelete = document.getElementById('confirmDelete');
    var cancelDelete = document.getElementById('cancelDelete');

    window.deleteUser = function(id_str) {
        id = parseInt(id_str)
        deleteUserModal.style.display = "block";
        var data = {'type': 'UserAccount', 'id': id}
        cancelDelete.onclick = function () {
            deleteUserModal.style.display = "none";
        }

        confirmDelete.onclick = function () {
            fetch('/delete/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                credentials: 'same-origin',
                body: JSON.stringify(data)
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        window.location.replace("/dashboard");
                    } else {
                        alert("There was an error deleting this account.");
                    }
                });
            deleteUserModal.style.display = "none";
        }
    }
}

function showNotification(message, isSuccess) {
    var notification = document.getElementById('notification');
    var messageElement = document.getElementById('notificationMessage');

    // Set the message and styles based on success or failure
    messageElement.textContent = message;
    notification.style.backgroundColor = isSuccess ? '#90ee90' : '#f08080'; // Green for success, red for failure
    notification.style.display = 'block';

    // Hide the notification after 3 seconds
    setTimeout(function() {
        notification.style.display = 'none';
    }, 3000);
}


document.getElementById('cancel-button').addEventListener('click', function() {
    document.getElementById('edit-form').style.display = 'none';
    document.getElementById('profile-info').style.display = 'block';
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

    var account_type = document.getElementById('account-type').textContent;
    var options = document.getElementById('edit-account-type')
    for (var i = 0; i < options.length; i++) {
        if (options[i].value === account_type) {
            options[i].selected = true;
            break;
        }
    }
});

function updateFields() {
    document.getElementById('first-name').innerText = document.getElementById('edit-first-name').value;
    document.getElementById('last-name').innerText = document.getElementById('edit-last-name').value;
    document.getElementById('username').innerText = document.getElementById('edit-username').value;
    document.getElementById('email').innerText = document.getElementById('edit-email').value;
    document.getElementById('account-type').innerText = document.getElementById('edit-account-type').value;
}

document.getElementById('save-button').addEventListener('click', function() {
    var allFields = document.querySelectorAll("#edit-form input");
    var allFieldsFilled = true;
    allFields.forEach(function(field) {
        if (!field.checkValidity()) {
            allFieldsFilled = false;
            field.classList.add("required");
        } else {
            field.classList.remove("required");
        }
    });

    // If any required field is empty, prevent saving and highlight the fields
    if (!allFieldsFilled) {
        showNotification('Please make fields are not blank and correct any errors.', false);
        return; // Exit the function, do not proceed with saving
    }

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
        account_type: document.getElementById('account-type').textContent
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
        updateFields();
        showNotification('Changes were successful.', true);
        window.history.replaceState({}, document.title, '/dashboard/users/'+document.getElementById('edit-username').value+'/');
    })
    .catch(error => {
        // Handle errors
        console.error('Error submitting profile changes:', error);
        showNotification('Changes were not successful.', false);
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

document.addEventListener("DOMContentLoaded", function() {
    var usernameInput = document.getElementById("edit-username");
    usernameInput.maxlength = "30";

    async function checkUsername() {
        var username = usernameInput.value.trim(); // Trim whitespace from the input

        var allowedPattern = /^[a-z0-9\-_.]{0,30}$/;

        if (username.length === 0) {
            usernameInput.style.borderColor = "";
            usernameInput.style.background = "";
        } else {
            if (!allowedPattern.test(username)) {
                // If not, prevent further input
                usernameInput.value = username.substring(0, username.length - 1);
            }

            if (username === document.getElementById("username").innerText) {
                usernameInput.style.borderColor = ""; // Reset to default
                usernameInput.style.background = "";
                return;
            }
            
            try {
                // Make an asynchronous request to check if the username exists
                var usernameExists = await check_username(username);
        
                // Change style of username input field based on whether the username exists
                if (usernameExists) {
                    usernameInput.style.borderColor = "red";
                    usernameInput.style.background = "red";
                } else {
                    usernameInput.style.borderColor = "green"; // Reset to default
                    usernameInput.style.background = "";
                }
            } catch (error) {
                console.error('Error checking username:', error);
                // Handle error here if needed
            }
        }
    }

    function enforceLowercase(event) {
        // Convert the input value to lowercase
        event.target.value = event.target.value.replace(/\s/g, '').toLowerCase();
    }

    // Listen for the "input" event and enforce lowercase
    usernameInput.addEventListener("input", enforceLowercase);
    
    usernameInput.addEventListener("input", checkUsername);    
});

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
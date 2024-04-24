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

function changePagingCount(selectedValue) {
    const preferences = {
        paging_count: selectedValue
    };

    fetch('/change_preferences/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken') // Include CSRF token if CSRF protection is enabled
    },
    body: JSON.stringify(preferences)
    })
    .then(response => {
        if (response.ok) {
            console.log('Preferences updated successfully');
            return response.json(); // Parse JSON response
        } else {
            console.error('Failed to update preferences');
            throw new Error('Failed to update preferences');
        }
    })
    .then(data => {
        console.log('Server response:', data);
        htmx.ajax('GET', '', '#request-data');
    })
    .catch(error => {
        console.error('Error:', error);
        // Handle error
    });
}

function sortRequestsTable(sort_by, columnIndex) {
    console.log(sort_by);
    var icon = document.getElementById("sort-icon-" + columnIndex);
    if(icon.classList.contains("bi-arrow-up")) {
        sort_by = '-' + sort_by;
        var ascending = false;
    } else {
        var ascending = true;
    }

    fetch('/change_preferences/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({'request_sort': sort_by})
    })
    .then(response => {
        if (response.ok) {
            console.log('Preferences updated successfully');
            return response.json(); // Parse JSON response
        } else {
            console.error('Failed to update preferences');
            throw new Error('Failed to update preferences');
        }
    })
    .then(data => {
        console.log('Server response:', data);
        for (var j = 0; j < 7; j++) {
            i = document.getElementById("sort-icon-" + j);
            i.classList.remove("bi-arrow-down", "bi-arrow-up");
        }
        icon.classList.add(ascending ? "bi-arrow-up" : "bi-arrow-down");
        htmx.ajax('GET', '.', '#request-data');
    })
    .catch(error => {
        console.error('Error:', error);
        // Handle error
    });
}

function sortUsersTable(sort_by, columnIndex) {
    console.log(sort_by);
    var icon = document.getElementById("sort-icon-" + columnIndex);
    if(icon.classList.contains("bi-arrow-up")) {
        sort_by = '-' + sort_by;
        var ascending = false;
    } else {
        var ascending = true;
    }

    fetch('/change_preferences/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({'user_sort': sort_by})
    })
    .then(response => {
        if (response.ok) {
            console.log('Preferences updated successfully');
            return response.json(); // Parse JSON response
        } else {
            console.error('Failed to update preferences');
            throw new Error('Failed to update preferences');
        }
    })
    .then(data => {
        console.log('Server response:', data);
        for (var j = 0; j < 5; j++) {
            i = document.getElementById("sort-icon-" + j);
            i.classList.remove("bi-arrow-down", "bi-arrow-up");
        }
        icon.classList.add(ascending ? "bi-arrow-up" : "bi-arrow-down");
        htmx.ajax('GET', '.', '#request-data');
    })
    .catch(error => {
        console.error('Error:', error);
        // Handle error
    });
}

function sortBuildingsTable(sort_by, columnIndex) {
    console.log(sort_by);
    var icon = document.getElementById("sort-icon-" + columnIndex);
    if(icon.classList.contains("bi-arrow-up")) {
        sort_by = '-' + sort_by;
        var ascending = false;
    } else {
        var ascending = true;
    }

    fetch('/change_preferences/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({'building_sort': sort_by})
    })
    .then(response => {
        if (response.ok) {
            console.log('Preferences updated successfully');
            return response.json(); // Parse JSON response
        } else {
            console.error('Failed to update preferences');
            throw new Error('Failed to update preferences');
        }
    })
    .then(data => {
        console.log('Server response:', data);
        for (var j = 0; j < 6; j++) {
            i = document.getElementById("sort-icon-" + j);
            i.classList.remove("bi-arrow-down", "bi-arrow-up");
        }
        icon.classList.add(ascending ? "bi-arrow-up" : "bi-arrow-down");
        htmx.ajax('GET', '.', '#request-data');
    })
    .catch(error => {
        console.error('Error:', error);
        // Handle error
    });
}
var modal = document.getElementById("editNoteModal");
var noteText = document.getElementById('noteText');
var saveNote = document.getElementById('saveNote');
var cancelNote = document.getElementById('cancelNote');
var currentNoteId;
var optionsMenuModal = document.getElementById("optionsMenuModal")

var deleteNoteModal = document.getElementById("deleteNoteModal");
var confirmDelete = document.getElementById('confirmDelete');
var cancelDelete = document.getElementById('cancelDelete');
var noteToDelete;
var fileIdToDelete;
var deleteFileModal = document.getElementById('deleteFileModal')

let csrftoken = getCookie('csrftoken');

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.getElementById("download").addEventListener("click", function() {
    var element = document.getElementById('to-export');

    // Use html2pdf to convert HTML to PDF
    html2pdf().set({ html2canvas: { scale: 2 },
        jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' },
        margin: [1, 1, 1, 1]
    }).from(element).save('exported_document.pdf');
});




var save_button = document.getElementById("save");
var request_id = save_button.getAttribute('request-id');
save_button.addEventListener("click", function() {
    toggle_save(request_id);
});


cancelNote.onclick = function() {
    modal.style.display = "none";
}

function editNote(noteId) {
    currentNoteId = noteId;
    noteText.value = document.getElementById('note_' + noteId).innerText;
    modal.style.display = "block";
}


window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

saveNote.onclick = function() {
    let newNoteText = noteText.value;
    if (newNoteText == null || newNoteText == "") {
        alert("You must enter a note!");
    } else {
        fetch('/request/edit_note/' + currentNoteId + '/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                'note_id': currentNoteId,
                'note_text': newNoteText,
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('note_' + currentNoteId).innerText = newNoteText;
            } else {
                alert("There was an error editing the note.");
            }
        });
    }
    modal.style.display = "none";
}


function deleteNote(noteId) {
    noteToDelete = noteId;
    deleteNoteModal.style.display = "block";
}

cancelDelete.onclick = function() {
    deleteNoteModal.style.display = "none";
}

confirmDelete.onclick = function() {
    var data = {'type': 'MaintenanceNotes', 'id': noteToDelete}
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
                window.location.reload();
            } else {
                alert("There was an error deleting the note.");
            }
        });
    deleteNoteModal.style.display = "none";
}


window.onload = function() {
    var deleteRequestModal = document.getElementById("deleteRequestModal");
    var confirmDelete = document.getElementById('confirmDelete1');
    var cancelDelete = document.getElementById('cancelDelete1');

    window.deleteRequest = function(id_str) {
        id = parseInt(id_str)
        deleteRequestModal.style.display = "block";
        var data = {'type': 'MaintenanceRequest', 'id': id}
        cancelDelete.onclick = function () {
            deleteRequestModal.style.display = "none";
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
                        alert("There was an error deleting the building.");
                    }
                });
            deleteRequestModal.style.display = "none";
        }
    }
}

function toggle_save(request_id) {
    // Send a POST request to the Django /toggle_save/request_id URL
    fetch('/toggle_save/'+request_id, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Get CSRF token from cookie
        },
        credentials: 'same-origin', // Include cookies in the request
    })
    .then(response => response.json())
    .then(data => {
        // Check if 'saved' key exists in the response
        if ('saved' in data) {
            // Get the bookmark icon element
            var bookmarkIcon = document.getElementById("bookmarkIcon");
            
            // Change the class of the bookmark icon based on the response
            if (data.saved) {
                bookmarkIcon.classList.remove("bi-bookmark");
                bookmarkIcon.classList.add("bi-bookmark-fill");
            } else {
                bookmarkIcon.classList.remove("bi-bookmark-fill");
                bookmarkIcon.classList.add("bi-bookmark");
            }
        } else {
            console.error('Response does not contain the "saved" key.');
        }
    })
    .catch(error => {
        console.error('Error toggling save:', error);
    });
    
}


function removeImage(imageId) {
    const csrftoken = getCookie('csrftoken'); // Function to get CSRF token from cookie
    fetch(`/remove_image/${imageId}/`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': csrftoken
        }
    })
    .then(response => {
        if (response.ok) {
            // Refresh the page or update the image container
            location.reload();
        } else {
            console.error('Failed to remove image');
        }
    })
    .catch(error => console.error('Error:', error));
}



// JavaScript to handle modal
document.addEventListener('DOMContentLoaded', function () {
    var modal = document.querySelector('.file-modal');
    var modalImg = document.querySelector('.file-modal-content');
    var fileImages = document.querySelectorAll('.file-image');
    var closeButton = document.querySelector('.file-close');

    fileImages.forEach(function (image) {
        image.addEventListener('click', function () {
            modal.style.display = 'block';
            modalImg.src = image.src;
            modalImg.style.maxWidth = 'unset'; // Override max-width property
            modalImg.style.width = '70%';
            modalImg.style.maxWidth = '70%';
            document.getElementById("container").style.overflow = "hidden";
        });
    });

    if (closeButton) {
        closeButton.addEventListener('click', function () {
            modal.style.display = 'none';
            document.getElementById("container").style.overflow = "auto";
        });
    }
});


var confirmDelete2 = document.getElementById('confirmDelete2');
var cancelDelete2 = document.getElementById('cancelDelete2');
function confirmDeleteFile(fileId) {
    // Store the ID of the file to be deleted in a variable
    fileIdToDelete = fileId;

    // Show the delete file confirmation modal
    deleteFileModal.style.display = "block";
}

// Event listener for cancel delete file button
cancelDelete2.onclick = function() {
    // Hide the delete file confirmation modal
    deleteFileModal.style.display = "none";
}

// Event listener for confirm delete file button
confirmDelete2.onclick = function() {
    // Call the removeImage function with the file ID to delete
    removeImage(fileIdToDelete);

    // Hide the delete file confirmation modal
    deleteFileModal.style.display = "none";
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
    document.getElementById('request-info').style.display = 'block';
});

document.getElementById('edit-button').addEventListener('click', function() {
    // Hide profile info, show edit form
    document.getElementById('request-info').style.display = 'none';
    document.getElementById('edit-form').style.display = 'block';
    
    // Populate edit fields with current info
    document.getElementById('edit-first-name').value = document.getElementById('first-name').innerText;
    document.getElementById('edit-last-name').value = document.getElementById('last-name').innerText;
    document.getElementById('edit-phone').value = document.getElementById('phone').innerText;
    var building = document.getElementById('building').getAttribute('building_id');
    var options = document.getElementById('edit-building');
    for (var i = 0; i < options.length; i++) {
        if (options[i].value === building) {
            options[i].selected = true;
            break;
        }
    }
    document.getElementById('edit-unit').value = document.getElementById('unit').innerText;
    var status = document.getElementById('status').innerText;
    var options = document.getElementById('edit-status');
    for (var i = 0; i < options.length; i++) {
        if (options[i].value === status) {
            options[i].selected = true;
            break;
        }
    }
    var priority = document.getElementById('priority').innerText;
    var options = document.getElementById('edit-priority');
    for (var i = 0; i < options.length; i++) {
        if (options[i].value === priority) {
            options[i].selected = true;
            break;
        }
    }

    document.getElementById('edit-title').value = document.getElementById('title').innerText;
    document.getElementById('edit-request').value = document.getElementById('request').innerText;
    var entry_permission = document.getElementById('entry-permission').innerText;
    var options = document.getElementById('edit-entry-permission');
    for (var i = 0; i < options.length; i++) {
        if (options[i].innerText === entry_permission) {
            options[i].selected = true;
            break;
        }
    }
});

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

    // Hide edit form, show profile info
    submitChanges();
});

function updateFields() {
    document.getElementById('first-name').innerText = document.getElementById('edit-first-name').value;
    document.getElementById('last-name').innerText = document.getElementById('edit-last-name').value;
    document.getElementById('phone').innerText = document.getElementById('edit-phone').value;

    var building = document.getElementById('building');
    var edit_building = document.getElementById('edit-building');
    building.innerText = edit_building.options[edit_building.selectedIndex].innerText;
    building.building_id = edit_building.value;
    building.href = '/dashboard/buildings/'+edit_building.value;

    document.getElementById('unit').innerText = document.getElementById('edit-unit').value;

    var status = document.getElementById('status');
    status.classList.remove(status.innerText.toLowerCase().replace(/\s/g, ''));
    status.innerText = document.getElementById('edit-status').value;
    status.classList.add(status.innerText.toLowerCase().replace(/\s/g, ''));

    var priority = document.getElementById('priority');
    priority.classList.remove(priority.innerText.toLowerCase().replace(/\s/g, ''));
    priority.innerText = document.getElementById('edit-priority').value;
    priority.classList.add(priority.innerText.toLowerCase().replace(/\s/g, ''));

    document.getElementById('title').innerText = document.getElementById('edit-title').value;
    document.getElementById('request').innerText = document.getElementById('edit-request').value;
    var edit_entry_permission = document.getElementById('edit-entry-permission');
    document.getElementById('entry-permission').innerText = edit_entry_permission.options[edit_entry_permission.selectedIndex].innerText;

    document.getElementById('edit-form').style.display = 'none';
    document.getElementById('request-info').style.display = 'block';
}

function submitChanges() {
    var updatedProfileData = {
        first_name: document.getElementById('edit-first-name').value,
        last_name: document.getElementById('edit-last-name').value,
        phone: document.getElementById('edit-phone').value,
        building: document.getElementById('edit-building').value,
        unit: document.getElementById('edit-unit').value,
        status: document.getElementById('edit-status').value,
        priority: document.getElementById('edit-priority').value,
        title: document.getElementById('edit-title').value,
        request: document.getElementById('edit-request').value,
        entry_permission: document.getElementById('edit-entry-permission').value,
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
        console.log(response.json());
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        // Handle successful response
        console.log('Changes submitted successfully');
        updateFields()
        // Call this function to show a success notification
        showNotification('Changes were successful.', true);

    })
    .catch(error => {
        // Handle errors
        console.error('Error submitting changes:', error);
        // Call this function to show a failure notification
        showNotification('Changes were not successful.', false);
    });
}
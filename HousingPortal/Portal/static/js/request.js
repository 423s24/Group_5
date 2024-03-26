var modal = document.getElementById("editNoteModal");
var span = document.getElementsByClassName("close")[0];
var noteText = document.getElementById('noteText');
var saveNote = document.getElementById('saveNote');
var cancelNote = document.getElementById('cancelNote');
var currentNoteId;

var deleteNoteModal = document.getElementById("deleteNoteModal");
var confirmDelete = document.getElementById('confirmDelete');
var cancelDelete = document.getElementById('cancelDelete');
var noteToDelete;

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


cancelNote.onclick = function() {
    modal.style.display = "none";
}

function editNote(noteId) {
    currentNoteId = noteId;
    noteText.value = document.getElementById('note_' + noteId).innerText;
    modal.style.display = "block";
}

span.onclick = function() {
    modal.style.display = "none";
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
    fetch('/request/delete_note/' + noteToDelete + '/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        }
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


function deleteRequest(id_str) {
    id = parseInt(id_str);

    var data = {
        type: 'MaintenanceRequest',
        id: id
    };

    var confirmed = window.confirm('Are you sure you want to delete this account?');
    if (confirmed) {
        fetch('/delete/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') // Get CSRF token from cookie
            },
            credentials: 'same-origin', // Include cookies in the request
            body: JSON.stringify(data) // Convert data to JSON format
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            // Handle successful response
            console.log('Delete success');
            //window.history.back();
            window.location.replace("/dashboard");
        })
        .catch(error => {
            // Handle errors
            console.error('Error submitting deleting:', error);
        });
    }
}
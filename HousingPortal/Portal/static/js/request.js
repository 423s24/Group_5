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
    html2canvas(element).then(function(canvas) {
        var imgData = canvas.toDataURL('image/png');
        var doc = new jsPDF('p', 'mm', 'a4');
        var pageWidth = doc.internal.pageSize.getWidth();
        var pageHeight = doc.internal.pageSize.getHeight();
        var imageWidth = canvas.width;
        var imageHeight = canvas.height;

        var widthRatio = pageWidth / imageWidth;
        var newHeight = imageHeight * widthRatio;
        var heightRatio = newHeight / pageHeight;

        doc.addImage(imgData, 'PNG', 5, 5, pageWidth-10, newHeight-10);

        // Open PDF in a new browser tab
        window.open(URL.createObjectURL(doc.output("blob")));
    });
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

    closeButton.addEventListener('click', function () {
        modal.style.display = 'none';
        document.getElementById("container").style.overflow = "auto";
    });
});




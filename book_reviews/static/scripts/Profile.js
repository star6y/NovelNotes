let Comment_Options = document.getElementsByClassName("Comment_button-container");

for(let i=0; i<Comment_Options.length;i++){
    Comment_Options[i].addEventListener("click",function(e){

    if (e.target.className === 'Delete_button'){
        let Comment_ID = parseInt(e.target.nextElementSibling.nextElementSibling.nextElementSibling.innerHTML);
    }

    else if (e.target.className === 'Edit_button'){
        let Comment_ID = parseInt(e.target.nextElementSibling.nextElementSibling.innerHTML);
        let text = e.target.parentElement.previousElementSibling.getElementsByClassName('comment-comment')[0].getElementsByTagName('textarea')[0];
        text.disabled = false;
        e.target.nextElementSibling.style.visibility = 'visible'
    }
    else if (e.target.className === 'Post_button'){
        let Comment_ID = parseInt(e.target.nextElementSibling.innerHTML)
    }
    })
};

// Flash messages
document.addEventListener("DOMContentLoaded", () => {
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        setTimeout(() => {
        message.style.display = 'none';
        }, 5000); // Hide after 5 seconds
    });
});

//  open modal to see whole review
function openReviewTextModal(title, text) {
    var decodedText = decodeURIComponent(text);
    document.getElementById('modal-title').innerText = title;
    document.getElementById('modal-text').innerHTML = decodedText; 
    document.getElementById('review-text-modal').style.display = 'block';
    openModal("review-text-modal");
}

function openCommentTextModal(text) {
    var decodedText = decodeURIComponent(text);  
    document.getElementById('com-modal-text').innerHTML = decodedText; 
    document.getElementById('comment-text-modal').style.display = 'block';
    openModal("comment-text-modal");
}


// window.addEventListener('click', function(event) {
//     var reviewTextModal = document.getElementById('review-text-modal');
//     var commentTextModal = document.getElementById('comment-text-modal');
   
//     if (event.target === reviewTextModal) {
//         closeModal('review-text-modal');
//     } else if (event.target === commentTextModal) {
//         closeModal('comment-text-modal');
//     }
// });
var ids = ["create-edit-review-modal", "confirm-delete-modal", "review-text-modal",
                 "comment-text-modal", "profile-picture-modal", "modal",
                 "create-edit-review-modal-content", "create-edit-comment-modal",
                "confirm-delete-comment-modal"]

var currentOpenModalId = null;
function openModal(modalId) {
    currentOpenModalId = modalId; 
}

// close modals by clicking outside of it
window.addEventListener('click', function(event) {
    let targetId = event.target.id; 
    if (ids.includes(targetId) ) {
        // console.log("closed it")
        closeModal(targetId);
    } 
});

// close modals by keyboard key 'esc'
window.addEventListener('keydown', function(event) {
    if (event.key === "Escape" && currentOpenModalId) {
        closeModal(currentOpenModalId);
    }
});



// review modals
function openEditReviewModal(id, title, reviewScore, reviewText) {
    var createEditModal= document.getElementById("create-edit-review-modal");
    var titleElem = document.getElementById("create-edit-review-title");
    var scoreInput = document.getElementById("review_score");
    var textArea = document.getElementById("review_text");
    var reviewIdInput = document.getElementById("review_id");
    createEditModal.querySelector('#review_output').textContent = reviewScore;

    createEditModal.style.display = "block";
    titleElem.innerText  = title;
    scoreInput.value = reviewScore;
    textArea.value = reviewText.replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&amp;/g, "&");
    reviewIdInput.value = id;
    openModal("create-edit-review-modal")
}

function openConfirmDeleteModal(id) {
    var confirmDeleteModal= document.getElementById("confirm-delete-modal");
    var reviewIdInput = document.getElementById("delete_review_id");

    reviewIdInput.value = id;
    confirmDeleteModal.style.display = "block";
    openModal("confirm-delete-modal")
}


// Close modal, element_id is given so we find the specific one
function closeModal(element_id) {
    var modal= document.getElementById(element_id);
    modal.style.display = "none";
    currentOpenModalId = null;
}


// comment modals
function openEditCommentModal(id, commentText) {
    var createEditModal= document.getElementById("create-edit-comment-modal");
    var textArea = document.getElementById("comment_text");
    var commentIdInput = document.getElementById("comment_id");

    createEditModal.style.display = "block";
    textArea.value = commentText.replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&amp;/g, "&");
    commentIdInput.value = id;
    openModal("create-edit-comment-modal")
}

function openConfirmCommentDeleteModal(id) {
    var confirmDeleteModal= document.getElementById("confirm-delete-comment-modal");
    var commentIdInput = document.getElementById("delete_comment_id");

    commentIdInput.value = id;
    confirmDeleteModal.style.display = "block";
    openModal("confirm-delete-comment-modal")
}

function redirect(url) {
    window.location.href = url;
}

function openProfilePictureModal() {
    var pfpPreview = document.getElementById("pfp-preview");
    var profilePictureModal = document.getElementById("profile-picture-modal");

    profilePictureModal.style.display = "block";
    pfpPreview.style.display = "none";
    openModal("profile-picture-modal")
}

function previewImage() {
    var input = document.getElementById('pfp-input');
    var preview = document.getElementById('pfp-preview');
    
    var file = input.files[0];
    if (file) {
        var reader = new FileReader();
        reader.onload = function (e) {
            preview.src = e.target.result;
        };
        reader.readAsDataURL(file);
        preview.style.display = 'block';
    } else {
        preview.src = '#';
        preview.style.display = 'none';
    }
}

const ratingInput = document.getElementById('review_score');
const ratingOutput = document.getElementById('review_output');

ratingInput.addEventListener('input', () => {
    ratingOutput.textContent = ratingInput.value;
});



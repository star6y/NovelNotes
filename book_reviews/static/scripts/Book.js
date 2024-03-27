// Modal scripts
const commentModal = document.getElementById("comment-modal");
const createEditReviewModal = document.getElementById("create-edit-review-modal");
const editCommentModal = document.getElementById("edit-comment-modal");
const confirmDeleteModal = document.getElementById("confirm-delete-modal");

function openCommentModal(review, sessionUser) {
    // Set reviewer info
    commentModal.querySelector('.profilePictureSmall').src = `/profilePicture/${review.reviewer.username}`;
    commentModal.querySelector('#user-link').textContent = `@${review.reviewer.username}`;
    commentModal.querySelector('#user-link').href = `/profile?Username=${review.reviewer.username}`

    // Set review info
    commentModal.querySelector('#review-score').textContent = "Score: " + review.review_score;
    commentModal.querySelector('#review-text').textContent = review.review_text;
    commentModal.querySelector('#review-created-at').textContent = review.review_created_at;
    if (review.review_created_at != review.review_updated_at) {
        commentModal.querySelector('#review-updated-at').textContent = `Edited: ${review.review_updated_at}`;
    } else {
        commentModal.querySelector('#review-updated-at').textContent = "";
    }

    // Remove previous edit/delete buttons
    var previousEditDelete = commentModal.querySelector('#review-card-edit-delete');
    if (previousEditDelete) {
        previousEditDelete.remove();
    }

    // Add edit/delete buttons if user is the reviewer
    if (!!sessionUser && review.reviewer.id == sessionUser.uid) {
        var reviewCard = commentModal.querySelector('.review-card');
        var reviewCardEditDelete = document.createElement('div');
        reviewCardEditDelete.id = "review-card-edit-delete";
        reviewCardEditDelete.classList.add('align-right');
        reviewCardEditDelete.classList.add('mt-20');

        reviewCardEditDelete.innerHTML = `
            <div>
                <button class="btn" id="modal-edit-review-btn">Edit</button>
                <button class="btn" onclick='openConfirmDeleteReviewModal("${review.book_id}")'>Delete</button>
            </div>
        `;
        reviewCardEditDelete.querySelector('#modal-edit-review-btn').addEventListener('click', function() {
            openCreateEditReviewModal(review.book_id, review);
        });
        reviewCard.appendChild(reviewCardEditDelete);
    }

    var reviewCardLikes = commentModal.querySelector('.review-card-likes');
    reviewCardLikes.innerHTML = `
            <div>
                <button id="modal-upvote" class="button-no-style" onclick="promptAuth()">⬆</button>
                <span id="modal-like-count">${review.total_likes}</span>
                <button id="modal-downvote" class="button-no-style" onclick="promptAuth()">⬇</button>
            </div>
        `;
    if (!!sessionUser) {
        var likeCount = document.getElementById(`like-count-${review.review_id}`);
        reviewCardLikes.querySelector('#modal-like-count').textContent = likeCount.textContent;

        var upvote = document.getElementById(`upvote-${review.review_id}`);
        var downvote = document.getElementById(`downvote-${review.review_id}`);

        var modalUpvote = reviewCardLikes.querySelector('#modal-upvote');
        var modalDownvote = reviewCardLikes.querySelector('#modal-downvote');

        modalUpvote.setAttribute('onclick', `likeReview(${review.review_id})`);
        modalDownvote.setAttribute('onclick', `dislikeReview(${review.review_id})`);

        if (upvote.classList.contains('color-upvote')) {
            modalUpvote.classList.add('color-upvote');
            modalUpvote.setAttribute('onclick', `unlikeReview(${review.review_id})`);
        } else if (downvote.classList.contains('color-downvote')) {
            modalDownvote.classList.add('color-downvote');
            modalDownvote.setAttribute('onclick', `undislikeReview(${review.review_id})`);
        }
    }

    var commentThread = commentModal.querySelector('#comment-thread');
    commentThread.innerHTML = "";

    review.comments.forEach(comment_str => {
        const comment = JSON.parse(comment_str);
        var commentCard = document.createElement('div');
        commentCard.classList.add('comment-card');
        commentCard.classList.add('soft-outline');
        commentCard.innerHTML = `
            <div class="space-between-start">
                <img class="profilePictureSmall" src="/profilePicture/${comment.commenter_username}">
                <div class="review-comment-content">
                    <div class="review-header">
                        <div class="author-heading">
                            <h3><a href="/profile?Username=${comment.commenter_username}" style="color: black; text-decoration: none;">@${comment.commenter_username}</a></h3>
                        </div>
                        <div class="timestamps align-right">
                            <p>${ comment.created_at }</p>
                        </div>
                    </div>
                    <p>${comment.text}</p>
                </div>
            </div>
        `;

        if (!!sessionUser && comment.commenter_id == sessionUser.uid) {
            var commentCardEditDelete = document.createElement('div');
            commentCardEditDelete.classList.add('align-right');
            commentCardEditDelete.classList.add('mt-20');
            commentCardEditDelete.innerHTML = `
                <button class="btn" id="edit-btn">Edit</button>
                <button class="btn" onclick='openConfirmDeleteCommentModal("${review.book_id}", ${comment.comment_id})'>Delete</button>
            `;
            commentCard.appendChild(commentCardEditDelete);
            commentCard.querySelector('#edit-btn').addEventListener('click', function() {
                openCommentEditModal(review.book_id, comment);
            });
        }

        var timestampsRight = commentCard.querySelector('.timestamps');
        if (comment.created_at != comment.updated_at) {
            var editedTimestamp = document.createElement('p');
            editedTimestamp.textContent = `Edited: ${comment.updated_at}`;
            timestampsRight.appendChild(editedTimestamp);
        }
        commentThread.appendChild(commentCard);
    });

    // Add comment form
    var commentForm = document.createElement('form');
    commentForm.id = "comment-form";
    commentForm.classList.add('pure-form');
    commentForm.method = "POST";
    commentForm.action = `/api/book/${review.book_id}/comment/${review.review_id}/post`;

    if (!!sessionUser) {
        commentForm.classList.add('comment-card');
        commentForm.classList.add('soft-outline');
        commentForm.innerHTML = `
            <h3>Share your thoughts!</h3>
            <textarea name="text" id="comment" class="comment-input pure-input-1" rows="5" required minlength="2" maxlength="400"></textarea>
            <button class="btn mt-20">Add Comment</button>
        `;
    } else {
        commentForm.innerHTML = `
            <div class="center-content">
                <h3><a href="/login">Log in</a> to add a comment</h3>
            </div>
        `;
    }
    commentThread.appendChild(commentForm);
    commentModal.style.display = "block";
    openModal("comment-modal");
}

function closeCommentModal() {
    commentModal.style.display = "none";
}

function openCreateEditReviewModal(bookId, review = undefined) {
    var form = createEditReviewModal.querySelector('#review-form');
    if (review) {
        form.action = `/api/book/${bookId}/review/edit`;
        createEditReviewModal.querySelector('#create-edit-review-title').textContent = "Edit Your Review";
        createEditReviewModal.querySelector('#review_score').value = review.review_score;
        createEditReviewModal.querySelector('#review_output').textContent = review.review_score;
        createEditReviewModal.querySelector('#review_text').value = review.review_text;
    } else {
        form.action = `/api/book/${bookId}/review/post`;
        createEditReviewModal.querySelector('#create-edit-review-title').textContent = "Write Your Review";
        createEditReviewModal.querySelector('#review_score').value = 3;
        createEditReviewModal.querySelector('#review_output').textContent = 3;
        createEditReviewModal.querySelector('#review_text').value = "";
    }
    createEditReviewModal.style.display = "block";
    openModal("create-edit-review-modal");
}

function closeReviewModal() {
    createEditReviewModal.style.display = "none";
}

function openCommentEditModal(bookId, comment) {
    editCommentModal.querySelector('#create-edit-comment-title').textContent = "Edit Your Comment";
    editCommentModal.querySelector('#comment_text').value = comment.text;
    editCommentModal.style.display = "block";
    editCommentModal.querySelector('#edit-comment-form').action = `/api/book/${bookId}/comment/${comment.comment_id}/edit`;
    openModal("create-edit-comment-modal");
}

function closeEditCommentModal() {
    editCommentModal.style.display = "none";
}

function openConfirmDeleteReviewModal(bookId) {
    confirmDeleteModal.querySelector('#delete-confirm-text').textContent = "Are you sure you want to delete your review?";
    confirmDeleteModal.querySelector('#delete-form').action = `/api/book/${bookId}/review/delete`;
    confirmDeleteModal.style.display = "block";
    openModal("confirm-delete-modal");
}

function openConfirmDeleteCommentModal(bookId, commentId) {
    confirmDeleteModal.querySelector('#delete-confirm-text').textContent = "Are you sure you want to delete your comment?";
    confirmDeleteModal.querySelector('#delete-form').action = `/api/book/${bookId}/comment/${commentId}/delete`;
    confirmDeleteModal.style.display = "block";
    openModal("confirm-delete-modal");
}

function closeConfirmDeleteModal() {
    confirmDeleteModal.style.display = "none";
}

function promptAuth() {
    alert("You must be logged in to do perform this action!");
}

// Star rating script
const ratingInput = document.getElementById('review_score');
const ratingOutput = document.getElementById('review_output');

ratingInput.addEventListener('input', () => {

    ratingOutput.textContent = ratingInput.value;
});

// Open comment modal from URL
const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
if (urlParams.has('review')) {
    const reviewId = urlParams.get('review');
    const openCommentModalButton = document.getElementById(`open-comment-modal-button-${reviewId}`);
    if (openCommentModalButton) {
        openCommentModalButton.click();
    }
}

var ids = ["create-edit-review-modal", "confirm-delete-modal", 
            "create-edit-comment-modal", "comment-modal"]
    
var currentOpenModalId = null;
function openModal(modalId) {
    currentOpenModalId = modalId; 
}

// close modals by clicking outside of it
window.addEventListener('click', function(event) {
    // let targetId = event.target.id; 
    if (event.target.id === "create-edit-review-modal") {
        closeReviewModal();
    } else if (event.target.id === "confirm-delete-modal") {
        closeConfirmDeleteModal();
    } else if (event.target.id === "create-edit-comment-modal" || event.target.id === "edit-comment-modal") {
        closeEditCommentModal();
    } else if (event.target.id === "comment-modal") {
        closeCommentModal();
    } else {}
});

// close modals by keyboard key 'esc'
window.addEventListener('keydown', function(event) {
    if (event.key === "Escape") {
        if (currentOpenModalId === "create-edit-review-modal") {
            closeReviewModal();
        } else if (currentOpenModalId === "confirm-delete-modal") {
            closeConfirmDeleteModal();
        } else if (currentOpenModalId === "create-edit-comment-modal") {
            closeEditCommentModal();
        } else if (currentOpenModalId === "comment-modal") {
            closeCommentModal();
        } else {}
    }
});

// Flash messages
document.addEventListener("DOMContentLoaded", () => {
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        setTimeout(() => {
        message.style.display = 'none';
        }, 5000); // Hide after 5 seconds
    });
});

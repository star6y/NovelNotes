function likeReview(reviewId) {
    var upvote = document.getElementById(`upvote-${reviewId}`);
    var downvote = document.getElementById(`downvote-${reviewId}`);
    var likeCount = document.getElementById(`like-count-${reviewId}`);
    var modalUpvote = document.getElementById('modal-upvote');
    var modalDownvote = document.getElementById('modal-downvote');
    var modalLikeCount = document.getElementById('modal-like-count');
    
    var wasDownvoted = downvote.classList.contains('color-downvote');
    upvote.classList.add('color-upvote');
    modalUpvote.classList.add('color-upvote');

    likes = parseInt(likeCount.textContent) + 1;

    if (wasDownvoted) {
        downvote.classList.remove('color-downvote');
        modalDownvote.classList.remove('color-downvote');
        likes += 1;
    }

    likeCount.textContent = likes;
    modalLikeCount.textContent = likes;

    fetch(`/api/book/review/${reviewId}/like`, {
        method: 'POST',
    })
        .then(_ => {
            upvote.setAttribute('onclick', `unlikeReview(${reviewId})`);
            modalUpvote.setAttribute('onclick', `unlikeReview(${reviewId})`);
            downvote.setAttribute('onclick', `dislikeReview(${reviewId})`);
            modalDownvote.setAttribute('onclick', `dislikeReview(${reviewId})`);
        })
        .catch(error => {
            console.log(error);
            
            likeCount.textContent = likes - 1;
            modalLikeCount.textContent = likes - 1;

            upvote.classList.remove('color-upvote');
            modalUpvote.classList.remove('color-upvote');
            if (wasDownvoted) {
                downvote.classList.add('color-downvote');
                modalDownvote.classList.add('color-downvote');
            }
            
            alert('An unexpected error occurred, please try again!');
        });
}

function dislikeReview(reviewId) {
    var upvote = document.getElementById(`upvote-${reviewId}`);
    var downvote = document.getElementById(`downvote-${reviewId}`);
    var likeCount = document.getElementById(`like-count-${reviewId}`);
    var modalUpvote = document.getElementById('modal-upvote');
    var modalDownvote = document.getElementById('modal-downvote');
    var modalLikeCount = document.getElementById('modal-like-count');

    var wasUpvoted = upvote.classList.contains('color-upvote');
    downvote.classList.add('color-downvote');
    modalDownvote.classList.add('color-downvote');

    likes = parseInt(likeCount.textContent) - 1;

    if (wasUpvoted) {
        upvote.classList.remove('color-upvote');
        modalUpvote.classList.remove('color-upvote');
        likes -= 1;
    }

    likeCount.textContent = likes;
    modalLikeCount.textContent = likes;

    fetch(`/api/book/review/${reviewId}/dislike`, {
        method: 'POST',
    })
        .then(_ => {
            downvote.setAttribute('onclick', `undislikeReview(${reviewId})`);
            modalDownvote.setAttribute('onclick', `undislikeReview(${reviewId})`);
            upvote.setAttribute('onclick', `likeReview(${reviewId})`);
            modalUpvote.setAttribute('onclick', `likeReview(${reviewId})`);
        })
        .catch(error => {
            console.log(error);

            likeCount.textContent = likes + 1;
            modalLikeCount.textContent = likes + 1;

            downvote.classList.remove('color-downvote');
            modalDownvote.classList.remove('color-downvote');
            if (wasUpvoted) {
                upvote.classList.add('color-upvote');
                modalUpvote.classList.add('color-upvote');
            }

            alert('An unexpected error occurred, please try again!');
        });
}

function unlikeReview(reviewId) {
    var upvote = document.getElementById(`upvote-${reviewId}`);
    var downvote = document.getElementById(`downvote-${reviewId}`);
    var likeCount = document.getElementById(`like-count-${reviewId}`);
    var modalUpvote = document.getElementById('modal-upvote');
    var modalDownvote = document.getElementById('modal-downvote');
    var modalLikeCount = document.getElementById('modal-like-count');

    upvote.classList.remove('color-upvote');
    modalUpvote.classList.remove('color-upvote');

    likes = parseInt(likeCount.textContent) - 1;
    likeCount.textContent = likes;
    modalLikeCount.textContent = likes;

    fetch(`/api/book/review/${reviewId}/unlike`, {
        method: 'DELETE',
    })
        .then(_ => {
            upvote.setAttribute('onclick', `likeReview(${reviewId})`);
            modalUpvote.setAttribute('onclick', `likeReview(${reviewId})`);
            downvote.setAttribute('onclick', `dislikeReview(${reviewId})`);
            modalDownvote.setAttribute('onclick', `dislikeReview(${reviewId})`);
        })
        .catch(error => {
            console.log(error);

            likeCount.textContent = likes + 1;
            modalLikeCount.textContent = likes + 1;

            upvote.classList.add('color-upvote');
            alert('An unexpected error occurred, please try again!');
        });
}

function undislikeReview(reviewId) {
    var upvote = document.getElementById(`upvote-${reviewId}`);
    var downvote = document.getElementById(`downvote-${reviewId}`);
    var likeCount = document.getElementById(`like-count-${reviewId}`);
    var modalUpvote = document.getElementById('modal-upvote');
    var modalDownvote = document.getElementById('modal-downvote');
    var modalLikeCount = document.getElementById('modal-like-count');

    downvote.classList.remove('color-downvote');
    modalDownvote.classList.remove('color-downvote');
    
    likes = parseInt(likeCount.textContent) + 1;
    likeCount.textContent = likes;
    modalLikeCount.textContent = likes;

    fetch(`/api/book/review/${reviewId}/undislike`, {
        method: 'DELETE',
    })
        .then(_ => {
            downvote.setAttribute('onclick', `dislikeReview(${reviewId})`);
            modalDownvote.setAttribute('onclick', `dislikeReview(${reviewId})`);

            upvote.setAttribute('onclick', `likeReview(${reviewId})`);
            modalUpvote.setAttribute('onclick', `likeReview(${reviewId})`);
        })
        .catch(error => {
            console.log(error);
            
            likeCount.textContent = likes - 1;
            modalLikeCount.textContent = likes - 1;

            downvote.classList.add('color-downvote');
            alert('An unexpected error occurred, please try again!');
        });
}

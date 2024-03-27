function suggestBooks(prompt, include_preferences) {
    fetch('/api/recommendBooks', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            prompt: prompt,
            include_preferences: include_preferences
        }),
    })
        .then(response => response.json())
        .then(data => {
            data["books"].forEach(book => {
                document.getElementById("suggested-books-list").innerHTML += createBookHtml(book);
            });
            document.getElementById("form-submit").disabled = false;
            document.getElementById("loading").style.display = "none";
        })
        .catch(error => {
            console.log(error);
            alert('An unexpected error occurred, please try again!');
        });
}

function createBookHtml(book) {
    return `
    <div class="pure-u-1-3">
        <div class="l-box">
            <a href="/book/${book.book_id}" class="text-decoration-none">
                <div class="book-card-medium height-auto border">
                    <div class="details-container">
                        <div class="thumbnail-container">
                            <img src="${book.thumbnail}" alt="Book cover">
                        </div>
                        <div class="center-content">
                            <div class="book-title">
                                ${book.title}
                            </div> 
                            <p class="hp-20">${book.rationale}</p>
                        </div>
                    </div>
                </div>
            </a>
        </div>  
    </div>
    `;
}

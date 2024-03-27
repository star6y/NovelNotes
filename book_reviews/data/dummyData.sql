INSERT INTO Users (email, username) VALUES ('user1@gmail.com', 'user1');
INSERT INTO Users (email, username) VALUES ('user2@gmail.com', 'user2');
INSERT INTO Users (email, username) VALUES ('user3@gmail.com', 'user3');

INSERT INTO Reviews (reviewer_id, book_id, review_text, review_score) VALUES (1, '_zSzAwAAQBAJ', 'This is a great book!', 5);   -- Hunger Games
INSERT INTO Reviews (reviewer_id, book_id, review_text, review_score) VALUES (2, 'KiszDwAAQBAJ', 'This is a terrible book!', 1); -- IT
INSERT INTO Reviews (reviewer_id, book_id, review_text, review_score) VALUES (3, 'GZAoAQAAIAAJ', 'This is an okay book!', 3); -- Harry Potter and the Deathly Hallows

INSERT INTO Likes (user_id, review_id, like_score) VALUES (1, 1, 1);
INSERT INTO Likes (user_id, review_id, like_score) VALUES (1, 2, 1);
INSERT INTO Likes (user_id, review_id, like_score) VALUES (2, 1, 1);
INSERT INTO Likes (user_id, review_id, like_score) VALUES (3, 2, 1);

INSERT INTO ReviewComments (user_id, review_id, comment_text) VALUES (1, 1, 'I agree!');
INSERT INTO ReviewComments (user_id, review_id, comment_text) VALUES (2, 1, 'I disagree!');
INSERT INTO ReviewComments (user_id, review_id, comment_text) VALUES (3, 1, 'I agree!');

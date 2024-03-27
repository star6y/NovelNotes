CREATE TABLE Users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  username VARCHAR(15) UNIQUE NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Reviews (
  id SERIAL PRIMARY KEY,
  reviewer_id INT NOT NULL,
  book_id VARCHAR(20) NOT NULL,
  review_text TEXT NOT NULL,
  review_score REAL NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT unique_pair_constraint UNIQUE (reviewer_id, book_id),
  CONSTRAINT check_review_score CHECK (review_score >= 0 AND review_score <= 5),
  CONSTRAINT review_text_length CHECK (2 <= LENGTH(review_text) AND LENGTH(review_text) <= 2000),
  FOREIGN KEY (reviewer_id) REFERENCES Users(id) ON DELETE CASCADE
);

CREATE TABLE Likes (
  user_id INT,
  review_id INT,
  like_score INT NOT NULL,
  PRIMARY KEY (user_id, review_id),
  FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE,
  FOREIGN KEY (review_id) REFERENCES Reviews(id) ON DELETE CASCADE,
  CHECK (like_score = 1 OR like_score = -1)
);

CREATE TABLE ReviewComments (
  id SERIAL PRIMARY KEY,
  user_id INT NOT NULL,
  review_id INT NOT NULL,
  comment_text TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE,
  FOREIGN KEY (review_id) REFERENCES Reviews(id) ON DELETE CASCADE,
  CONSTRAINT comment_text_length CHECK (LENGTH(comment_text) BETWEEN 2 AND 400)
);

CREATE TABLE Images (
  user_id SERIAL PRIMARY KEY,
  image_bytes BYTEA NOT NULL,
  FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
);

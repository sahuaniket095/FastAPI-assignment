CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR UNIQUE NOT NULL,
    hashed_password VARCHAR NOT NULL,
    role VARCHAR CHECK (role IN ('admin', 'participant')) NOT NULL
);

CREATE TABLE quizzes (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    description VARCHAR NOT NULL,
    created_by INTEGER REFERENCES users(id) NOT NULL
);

CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    quiz_id INTEGER REFERENCES quizzes(id) NOT NULL,
    statement VARCHAR NOT NULL,
    options JSON NOT NULL,  -- Stores answer options as JSON (e.g., {"A": "Option A", "B": "Option B"})
    correct_answer VARCHAR NOT NULL
);

CREATE TABLE submissions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) NOT NULL,
    quiz_id INTEGER REFERENCES quizzes(id) NOT NULL,
    score REAL NOT NULL,  -- Percentage score
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE submission_answers (
    id SERIAL PRIMARY KEY,
    submission_id INTEGER REFERENCES submissions(id) NOT NULL,
    question_id INTEGER REFERENCES questions(id) NOT NULL,
    selected_answer VARCHAR NOT NULL
);
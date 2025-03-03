-- Users table: Stores user information
CREATE TABLE users (
    id SERIAL PRIMARY KEY, -- Unique user ID
    username VARCHAR UNIQUE NOT NULL, -- Unique username
    hashed_password VARCHAR NOT NULL, -- Encrypted password
    role VARCHAR CHECK (role IN ('admin', 'participant')) NOT NULL -- User role constraint
);

-- Quizzes table: Stores quiz details
CREATE TABLE quizzes (
    id SERIAL PRIMARY KEY, -- Unique quiz ID
    title VARCHAR NOT NULL, -- Quiz title
    description VARCHAR NOT NULL, -- Quiz description
    created_by INTEGER REFERENCES users(id) NOT NULL -- Creator (admin) of the quiz
);

-- Questions table: Stores questions for quizzes
CREATE TABLE questions (
    id SERIAL PRIMARY KEY, -- Unique question ID
    quiz_id INTEGER REFERENCES quizzes(id) NOT NULL, -- Associated quiz ID
    statement VARCHAR NOT NULL, -- Question text
    options JSON NOT NULL,  -- Available answer choices in JSON format
    correct_answer VARCHAR NOT NULL -- Correct answer
);

-- Submissions table: Stores quiz attempt details
CREATE TABLE submissions (
    id SERIAL PRIMARY KEY, -- Unique submission ID
    user_id INTEGER REFERENCES users(id) NOT NULL, -- User who submitted the quiz
    quiz_id INTEGER REFERENCES quizzes(id) NOT NULL, -- Associated quiz ID
    score REAL NOT NULL,  -- Percentage score obtained
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Submission timestamp
);

-- Submission Answers table: Stores individual answers for each submission
CREATE TABLE submission_answers (
    id SERIAL PRIMARY KEY, -- Unique submission answer ID
    submission_id INTEGER REFERENCES submissions(id) NOT NULL, -- Associated submission ID
    question_id INTEGER REFERENCES questions(id) NOT NULL, -- Question ID
    selected_answer VARCHAR NOT NULL -- User's selected answer
);


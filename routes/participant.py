from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.quiz import Quiz
from models.question import Question
from models.submission import Submission
from models.submission_answer import SubmissionAnswer
from schemas.quiz import QuizOut
from schemas.submission import SubmissionCreate, SubmissionResult, AnswerResult
from utils.security import get_current_participant
from typing import List

# Creating an API router for participant-related actions
router = APIRouter(prefix="/participant", tags=["participant"])

# ------------------- Get all available quizzes -------------------
@router.get("/quizzes", response_model=List[QuizOut])
def get_quizzes(
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_participant)
):
    """
    Fetch all available quizzes along with their questions.
    """
    quizzes = db.query(Quiz).all()  # Fetch all quizzes from the database
    
    # Fetch questions for each quiz
    for quiz in quizzes:
        quiz.questions = db.query(Question).filter(Question.quiz_id == quiz.id).all()

    return quizzes  # Return quizzes along with their questions

# ------------------- Submit quiz answers -------------------
@router.post("/submit", response_model=SubmissionResult)
def submit_quiz(
    submission: SubmissionCreate, 
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_participant)
):
    """
    Submit quiz answers.
    - Validates if all questions are answered.
    - Checks if answers are valid.
    - Calculates score.
    - Stores the submission and answers in the database.
    """
    # Check if quiz exists
    quiz = db.query(Quiz).filter(Quiz.id == submission.quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    # Fetch all questions for the given quiz
    questions = db.query(Question).filter(Question.quiz_id == submission.quiz_id).all()
    question_ids = [q.id for q in questions]

    # Ensure all questions are answered
    if set(submission.answers.keys()) != set(question_ids):
        raise HTTPException(status_code=400, detail="Answer all questions")

    # Calculate score and validate answers
    correct_count = 0
    answers_list = []

    for q in questions:
        selected_answer = submission.answers[q.id]

        # Validate if the selected answer is a valid option
        if selected_answer not in q.options:
            raise HTTPException(status_code=400, detail=f"Invalid answer for question {q.id}")

        # Check if the answer is correct
        if selected_answer == q.correct_answer:
            correct_count += 1

        # Store the answer result
        answers_list.append(
            AnswerResult(
                question_id=q.id, 
                selected_answer=selected_answer, 
                correct_answer=q.correct_answer
            )
        )

    # Calculate the score as a percentage
    score = (correct_count / len(questions)) * 100  

    # Save the submission in the database
    new_submission = Submission(
        user_id=current_user["id"], 
        quiz_id=submission.quiz_id, 
        score=score
    )
    db.add(new_submission)
    db.commit()
    db.refresh(new_submission)

    # Save each answer in the database
    for answer in answers_list:
        db.add(SubmissionAnswer(
            submission_id=new_submission.id, 
            question_id=answer.question_id, 
            selected_answer=answer.selected_answer
        ))

    db.commit()  # Commit the changes

    return SubmissionResult(score=score, answers=answers_list)

# ------------------- Get quiz result -------------------
@router.get("/result/{quiz_id}", response_model=SubmissionResult)
def get_result(
    quiz_id: int, 
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_participant)
):
    """
    Retrieve quiz results for the participant.
    - Fetches the participant's submission for the given quiz.
    - Retrieves the selected and correct answers.
    """
    # Fetch the submission for the quiz and the current user
    submission = db.query(Submission).filter(
        Submission.quiz_id == quiz_id, 
        Submission.user_id == current_user["id"]
    ).first()

    if not submission:
        raise HTTPException(status_code=404, detail="No submission found")

    # Fetch all answers for this submission
    answers = db.query(SubmissionAnswer).filter(SubmissionAnswer.submission_id == submission.id).all()
    result_answers = []

    # Retrieve correct answers for each question
    for answer in answers:
        question = db.query(Question).filter(Question.id == answer.question_id).first()
        result_answers.append(
            AnswerResult(
                question_id=answer.question_id,
                selected_answer=answer.selected_answer,
                correct_answer=question.correct_answer
            )
        )

    # Return the submission result with the score and answers
    return SubmissionResult(score=submission.score, answers=result_answers)

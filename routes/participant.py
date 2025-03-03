# routes/participant.py
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

router = APIRouter(prefix="/participant", tags=["participant"])

# Get all available quizzes with their questions
@router.get("/quizzes", response_model=List[QuizOut])
def get_quizzes(db: Session = Depends(get_db), current_user: dict = Depends(get_current_participant)):
    # Fetch all quizzes
    quizzes = db.query(Quiz).all()
    # For each quiz, fetch its questions
    for quiz in quizzes:
        quiz.questions = db.query(Question).filter(Question.quiz_id == quiz.id).all()
    return quizzes

# Submit quiz answers
@router.post("/submit", response_model=SubmissionResult)
def submit_quiz(submission: SubmissionCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_participant)):
    # Check if quiz exists
    quiz = db.query(Quiz).filter(Quiz.id == submission.quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    # Get all questions
    questions = db.query(Question).filter(Question.quiz_id == submission.quiz_id).all()
    question_ids = [q.id for q in questions]
    # Validate all questions answered
    if set(submission.answers.keys()) != set(question_ids):
        raise HTTPException(status_code=400, detail="Answer all questions")
    # Calculate score and validate answers
    correct_count = 0
    answers_list = []
    for q in questions:
        selected = submission.answers[q.id]
        if selected not in q.options:
            raise HTTPException(status_code=400, detail=f"Invalid answer for question {q.id}")
        if selected == q.correct_answer:
            correct_count += 1
        answers_list.append(AnswerResult(question_id=q.id, selected_answer=selected, correct_answer=q.correct_answer))
    score = (correct_count / len(questions)) * 100  # Percentage
    # Save submission
    new_submission = Submission(user_id=current_user["id"], quiz_id=submission.quiz_id, score=score)
    db.add(new_submission)
    db.commit()
    db.refresh(new_submission)
    # Save answers
    for answer in answers_list:
        db.add(SubmissionAnswer(submission_id=new_submission.id, question_id=answer.question_id, selected_answer=answer.selected_answer))
    db.commit()
    return SubmissionResult(score=score, answers=answers_list)

# Get quiz result
@router.get("/result/{quiz_id}", response_model=SubmissionResult)
def get_result(quiz_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_participant)):
    submission = db.query(Submission).filter(Submission.quiz_id == quiz_id, Submission.user_id == current_user["id"]).first()
    if not submission:
        raise HTTPException(status_code=404, detail="No submission found")
    answers = db.query(SubmissionAnswer).filter(SubmissionAnswer.submission_id == submission.id).all()
    result_answers = []
    for answer in answers:
        question = db.query(Question).filter(Question.id == answer.question_id).first()
        result_answers.append(AnswerResult(
            question_id=answer.question_id,
            selected_answer=answer.selected_answer,
            correct_answer=question.correct_answer
        ))
    return SubmissionResult(score=submission.score, answers=result_answers)
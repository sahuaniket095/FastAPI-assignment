from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.quiz import Quiz
from models.question import Question
from schemas.quiz import QuizCreate, QuizOut
from schemas.question import QuestionCreate, QuestionOut
from utils.security import get_current_admin

router = APIRouter(prefix="/admin", tags=["admin"])

# Creating a new quiz
@router.post("/quizzes", response_model=QuizOut)
def create_quiz(quiz: QuizCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_admin)):
    new_quiz = Quiz(title=quiz.title, description=quiz.description, created_by=current_user["id"])
    db.add(new_quiz)
    db.commit()
    db.refresh(new_quiz)
    return new_quiz

# Deleting a quiz
@router.delete("/quizzes/{quiz_id}")
def delete_quiz(quiz_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_admin)):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    # Only the creator can delete their quiz
    if quiz.created_by != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not your quiz")
    db.delete(quiz)
    db.commit()
    return {"message": "Quiz deleted"}

# Creating a new question
@router.post("/questions", response_model=QuestionOut)
def create_question(question: QuestionCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_admin)):
    quiz = db.query(Quiz).filter(Quiz.id == question.quiz_id).first()
    if not quiz or quiz.created_by != current_user["id"]:
        raise HTTPException(status_code=403, detail="Invalid quiz or not your quiz")
    new_question = Question(
        statement=question.statement,
        options=question.options,
        correct_answer=question.correct_answer,
        quiz_id=question.quiz_id
    )
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    return new_question

# Updating a question
@router.put("/questions/{question_id}", response_model=QuestionOut)
def update_question(question_id: int, question: QuestionCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_admin)):
    q = db.query(Question).filter(Question.id == question_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    quiz = db.query(Quiz).filter(Quiz.id == q.quiz_id).first()
    if quiz.created_by != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not your quiz")
    q.statement = question.statement
    q.options = question.options
    q.correct_answer = question.correct_answer
    q.quiz_id = question.quiz_id
    db.commit()
    db.refresh(q)
    return q

# Deleting a question
@router.delete("/questions/{question_id}")
def delete_question(question_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_admin)):
    q = db.query(Question).filter(Question.id == question_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    quiz = db.query(Quiz).filter(Quiz.id == q.quiz_id).first()
    if quiz.created_by != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not your quiz")
    db.delete(q)
    db.commit()
    return {"message": "Question deleted"}
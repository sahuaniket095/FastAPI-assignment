from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.quiz import Quiz
from models.question import Question
from schemas.quiz import QuizCreate, QuizOut
from schemas.question import QuestionCreate, QuestionOut
from utils.security import get_current_admin

# Create an API router for admin-specific endpoints
router = APIRouter(prefix="/admin", tags=["admin"])

# ------------------- Creating a new quiz -------------------
@router.post("/quizzes", response_model=QuizOut)
def create_quiz(
    quiz: QuizCreate, 
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_admin)
):
    """
    Create a new quiz.
    Only an admin user can create a quiz.
    """
    # Create a new quiz instance
    new_quiz = Quiz(
        title=quiz.title, 
        description=quiz.description, 
        created_by=current_user["id"]  # Assign the creator's ID
    )
    db.add(new_quiz)  # Add the quiz to the database session
    db.commit()  # Commit changes to the database
    db.refresh(new_quiz)  # Refresh the quiz instance to reflect new changes
    return new_quiz  # Return the newly created quiz

# ------------------- Deleting a quiz -------------------
@router.delete("/quizzes/{quiz_id}")
def delete_quiz(
    quiz_id: int, 
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_admin)
):
    """
    Delete a quiz by its ID.
    Only the creator of the quiz can delete it.
    """
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    
    if not quiz:  # If the quiz does not exist, return 404 error
        raise HTTPException(status_code=404, detail="Quiz not found")

    if quiz.created_by != current_user["id"]:  # Ensure only the creator can delete
        raise HTTPException(status_code=403, detail="Not your quiz")

    db.delete(quiz)  # Delete the quiz
    db.commit()  # Commit the deletion
    return {"message": "Quiz deleted"}

# ------------------- Creating a new question -------------------
@router.post("/questions", response_model=QuestionOut)
def create_question(
    question: QuestionCreate, 
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_admin)
):
    """
    Create a new question under a quiz.
    The quiz must exist and belong to the current admin.
    """
    quiz = db.query(Quiz).filter(Quiz.id == question.quiz_id).first()

    if not quiz or quiz.created_by != current_user["id"]:
        raise HTTPException(status_code=403, detail="Invalid quiz or not your quiz")

    # Create a new question instance
    new_question = Question(
        statement=question.statement,
        options=question.options,
        correct_answer=question.correct_answer,
        quiz_id=question.quiz_id
    )

    db.add(new_question)  # Add the question to the database session
    db.commit()  # Commit the transaction
    db.refresh(new_question)  # Refresh to reflect new changes
    return new_question  # Return the created question

# ------------------- Updating a question -------------------
@router.put("/questions/{question_id}", response_model=QuestionOut)
def update_question(
    question_id: int, 
    question: QuestionCreate, 
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_admin)
):
    """
    Update an existing question.
    Only the admin who created the quiz can update its questions.
    """
    q = db.query(Question).filter(Question.id == question_id).first()

    if not q:  # If the question does not exist, return 404 error
        raise HTTPException(status_code=404, detail="Question not found")

    quiz = db.query(Quiz).filter(Quiz.id == q.quiz_id).first()

    if quiz.created_by != current_user["id"]:  # Ensure only the quiz creator can update
        raise HTTPException(status_code=403, detail="Not your quiz")

    # Update the question details
    q.statement = question.statement
    q.options = question.options
    q.correct_answer = question.correct_answer
    q.quiz_id = question.quiz_id

    db.commit()  # Save changes
    db.refresh(q)  # Refresh the question instance
    return q  # Return the updated question

# ------------------- Deleting a question -------------------
@router.delete("/questions/{question_id}")
def delete_question(
    question_id: int, 
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_admin)
):
    """
    Delete a question by its ID.
    Only the admin who created the quiz can delete its questions.
    """
    q = db.query(Question).filter(Question.id == question_id).first()

    if not q:  # If the question does not exist, return 404 error
        raise HTTPException(status_code=404, detail="Question not found")

    quiz = db.query(Quiz).filter(Quiz.id == q.quiz_id).first()

    if quiz.created_by != current_user["id"]:  # Ensure only the quiz creator can delete
        raise HTTPException(status_code=403, detail="Not your quiz")

    db.delete(q)  # Delete the question
    db.commit()  # Commit the deletion
    return {"message": "Question deleted"}

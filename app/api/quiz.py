from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user_email, require_role
from app.models.subject import Subject, Topic
from app.models.question import Question
from app.schemas.quiz import QuestionForQuiz, SubjectCreate, SubjectResponse, TopicCreate, TopicResponse, QuestionCreate, QuestionResponse, AnswerSubmit, QuizSubmit
from typing import List

router = APIRouter()

# ============ SUBJECTS ============

@router.post("/subjects", response_model=SubjectResponse)
def create_subject(
    subject: SubjectCreate,
    current_user = Depends(require_role("teacher")),
    db: Session = Depends(get_db)
):
    db_subject = Subject(name=subject.name, description=subject.description)
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject

@router.get("/subjects", response_model=List[SubjectResponse])
def get_subjects(db: Session = Depends(get_db)):
    return db.query(Subject).all()

# ============ TOPICS ============

@router.post("/topics", response_model=TopicResponse)
def create_topic(
    topic: TopicCreate,
    current_user = Depends(require_role("teacher")),
    db: Session = Depends(get_db)
):
    db_topic = Topic(
        name=topic.name,
        subject_id=topic.subject_id,
        difficulty_level=topic.difficulty_level
    )
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic

# ============ QUESTIONS ============

@router.post("/questions", response_model=QuestionResponse)
def create_question(
    question: QuestionCreate,
    current_user = Depends(require_role("teacher")),
    db: Session = Depends(get_db)
):
    db_question = Question(
        topic_id=question.topic_id,
        question_text=question.question_text,
        option_a=question.option_a,
        option_b=question.option_b,
        option_c=question.option_c,
        option_d=question.option_d,
        correct_option=question.correct_option,
        difficulty_level=question.difficulty_level
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

@router.get("/topics/{topic_id}/questions", response_model=list[QuestionForQuiz])
def get_quiz_questions(
    topic_id: int,
    current_user = Depends(get_current_user_email),
    db: Session = Depends(get_db)
):
    questions = db.query(Question).filter(Question.topic_id == topic_id).all()
    if not questions:
        raise HTTPException(status_code=404, detail="No questions found for this topic")
    return questions

# ============ SUBMIT QUIZ ============

@router.post("/submit-quiz")
def submit_quiz(
    quiz_data: QuizSubmit,
    current_user_email: str = Depends(get_current_user_email),
    db: Session = Depends(get_db)
):
    from app.models.question import Question
    from app.models.user import User
    from app.models.quiz import QuizAttempt
    
    user = db.query(User).filter(User.email == current_user_email).first()
    
    score = 0
    total = len(quiz_data.answers)
    
    for answer in quiz_data.answers:
        question = db.query(Question).filter(Question.id == answer.question_id).first()
        if question and question.correct_option == answer.selected_option:
            score += 1
    
    percentage = (score / total * 100) if total > 0 else 0
    
    attempt = QuizAttempt(
        user_id=user.id,
        topic_id=quiz_data.topic_id,
        score=score,
        total_questions=total,
        percentage=percentage
    )
    db.add(attempt)
    db.commit()
    
    return {"score": score, "total": total, "percentage": round(percentage, 2)}
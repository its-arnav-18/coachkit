from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user_email, require_role
from app.models.subject import Subject, Topic
from app.models.question import Question
from app.schemas.quiz import SubjectCreate, SubjectResponse, TopicCreate, TopicResponse, QuestionCreate, QuestionResponse
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
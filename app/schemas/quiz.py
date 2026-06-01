from pydantic import BaseModel
from typing import Optional

class SubjectCreate(BaseModel):
    name: str
    description: Optional[str] = None

class SubjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True

class TopicCreate(BaseModel):
    name: str
    subject_id: int
    difficulty_level: int = 1

class TopicResponse(BaseModel):
    id: int
    name: str
    subject_id: int
    difficulty_level: int

    class Config:
        from_attributes = True

class QuestionCreate(BaseModel):
    topic_id: int
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_option: str
    difficulty_level: int = 1

class QuestionResponse(BaseModel):
    id: int
    topic_id: int
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    difficulty_level: int

    class Config:
        from_attributes = True

class QuestionForQuiz(BaseModel):
    id: int
    topic_id: int
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    difficulty_level: int

    class Config:
        from_attributes = True

class AnswerSubmit(BaseModel):
    question_id: int
    selected_option: str

class QuizSubmit(BaseModel):
    topic_id: int
    answers: list[AnswerSubmit]
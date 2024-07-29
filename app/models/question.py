from pydantic import BaseModel, field_validator

class QuestionSchema(BaseModel):
    question: str

    @field_validator('question')
    def check_question_length(cls, value):
        if len(value) < 10:
            raise ValueError('Question must be at least 10 characters long')
        return value
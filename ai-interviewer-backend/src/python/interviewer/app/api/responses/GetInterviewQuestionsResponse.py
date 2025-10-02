from pydantic import BaseModel

class GetInterviewQuestionsResponse(BaseModel):
    class QuestionResponse(BaseModel):
        question_id: int
        question_number: int
        part_no: int
        question_statement: str

        def __init__(self, question_id: int, question_number: int, part_no: int, question_statement: str):
            self.question_id = question_id
            self.question_number = question_number
            self.part_no = part_no
            self.question_statement = question_statement

    questions: list[QuestionResponse]

    def __init__(self, questions: list[QuestionResponse]):
        self.questions = questions

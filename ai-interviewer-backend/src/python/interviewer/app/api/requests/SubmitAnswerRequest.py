class SubmitAnswerRequest:
    interview_id: int
    question_no: int
    answer: str

    def validate(self):
        if self.interview_id < 1:
            raise ValueError("Interview id must be greater than 0")
        if self.question_no < 1:
            raise ValueError("Question no must be greater than 0")
        if not self.answer or len(self.answer.strip()) == 0:
            raise ValueError("Answer is invalid")
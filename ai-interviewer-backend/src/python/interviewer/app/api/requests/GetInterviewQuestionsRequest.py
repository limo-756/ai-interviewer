from interviewer.app.api.requests.BaseRequest import BaseRequest


class GetInterviewQuestionsRequest(BaseRequest):
    interview_id: int
    question_no: int
    all_questions: bool

    def validate(self):
        if self.interview_id < 1:
            raise ValueError("Interview id must be greater than 0")
        if self.all_questions:
            return
        if self.question_no < 1:
            raise ValueError("Question number must be greater than 0")

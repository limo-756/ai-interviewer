from interviewer.app.api.requests.BaseRequest import BaseRequest


class StartInterviewRequest(BaseRequest):
    topic: str
    resumeFile: str
    number_of_questions: int
    number_of_follow_up_questions: int
    duration_in_mins: int

    def validate(self):
        if not self.topic or len(self.topic.strip()) == 0:
            raise ValueError("Topic is invalid")
        if self.number_of_questions < 1:
            raise ValueError("Number of questions must be greater than 0")
        if self.number_of_follow_up_questions < 1:
            raise ValueError("Number of follow up questions must be greater than 0")
        if self.duration_in_mins < 1:
            raise ValueError("Duration in mins must be greater than 0")

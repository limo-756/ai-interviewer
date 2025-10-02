from pydantic import BaseModel

class StartInterviewResponse(BaseModel):
    interview_id: int
    interviewer_name: str
    total_questions: int
    number_of_follow_up_questions: int
    total_duration_in_mins: int

    def __init__(self,
                 interview_id: int,
                 interviewer_name: str,
                 total_questions: int,
                 number_of_follow_up_questions: int,
                 total_duration_in_mins: int):
        self.interview_id = interview_id
        self.interviewer_name = interviewer_name
        self.total_questions = total_questions
        self.number_of_follow_up_questions = number_of_follow_up_questions
        self.total_duration_in_mins = total_duration_in_mins
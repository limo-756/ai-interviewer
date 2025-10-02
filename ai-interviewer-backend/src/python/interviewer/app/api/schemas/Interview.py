import datetime

from interviewer.app.api.schemas.InterviewState import InterviewState


class Interview:
    interview_id: int
    user_id: int
    chat_id: int
    topic: str
    start_time: datetime
    end_time: datetime
    state: InterviewState
    number_of_questions: int
    number_of_follow_up_questions: int

    def __init__(self,
                 interview_id: int,
                 user_id: int,
                 chat_id: int,
                 topic: str,
                 start_time: datetime,
                 end_time: datetime,
                 state: InterviewState,
                 number_of_questions: int,
                 number_of_follow_up_questions: int):
        self.interview_id = interview_id
        self.user_id = user_id
        self.chat_id = chat_id
        self.topic = topic
        self.start_time = start_time
        self.end_time = end_time
        self.state = state
        self.number_of_questions = number_of_questions
        self.number_of_follow_up_questions = number_of_follow_up_questions
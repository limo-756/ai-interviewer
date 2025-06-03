import datetime


class Interview:
    interview_id: int
    user_id: int
    chat_id: int
    topic: str
    start_time: datetime.time
    end_time: datetime.time
    state: str

    def __init__(self,
                 interview_id: int,
                 user_id: int,
                 chat_id: int,
                 topic: str,
                 start_time: datetime.time,
                 end_time: datetime.time,
                 state: str):
        self.interview_id = interview_id
        self.user_id = user_id
        self.chat_id = chat_id
        self.topic = topic
        self.start_time = start_time
        self.end_time = end_time
        self.state = state
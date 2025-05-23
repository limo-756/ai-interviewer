import datetime


class Interview:
    interview_id: int
    user_id: int
    chat_id: int
    topic: str
    start_time: datetime.time
    end_time: datetime.time
    state: str
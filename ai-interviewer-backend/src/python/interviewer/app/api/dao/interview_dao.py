from sqlalchemy.orm import Session

from interviewer import models
from interviewer.app.api.schemas.Interview import Interview
import datetime


class InterviewDao:

    def __init__(self, db: Session):
       self.db = db

    def get_interview_by_id(self, interview_id: int) -> Interview:
        return (self.db.query(models.InterviewModel)
                .filter(models.InterviewModel.interview_id.key == interview_id)
                .first())

    def create_interview(self, topic:str, user_id:int, chat_id:int) -> Interview:
        db_item = models.InterviewModel(topic=topic, user_id=user_id, chat_id=chat_id,
                                        end_time=datetime.datetime.now() + datetime.timedelta(hours=1),
                                        state="SCHEDULED")
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item



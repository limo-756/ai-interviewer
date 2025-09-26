from typing import List

from sqlalchemy.orm import Session

from interviewer import models
from interviewer.app.api.schemas.Interview import Interview
import datetime

from interviewer.app.api.schemas.InterviewState import InterviewState
from interviewer.app.api.schemas.user import User


class InterviewDao:

    def __init__(self, db: Session):
        self.db = db

    def get_interview_by_id(self, interview_id: int) -> Interview:
        interview = (self.db.query(models.InterviewModel)
                     .filter(models.InterviewModel.interview_id.key == interview_id)
                     .first())
        return interview.to_interview()

    def get_all_interviews_for_user(self, user: User) -> List[User]:
        interview_models = (self.db.query(models.InterviewModel)
                     .filter(models.InterviewModel.user_id.key == user.user_id)
                     .to_list())

        interviews = []
        for model in interview_models:
            interviews.append(model.to_interview())
        return interviews


    def create_interview(self, topic: str, user_id: int) -> Interview:
        db_item = models.InterviewModel(topic=topic, user_id=user_id,
                                        end_time=datetime.datetime.now() + datetime.timedelta(hours=1),
                                        state=InterviewState.RUNNING.value)
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item.to_interview()

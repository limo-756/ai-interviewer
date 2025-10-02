from typing import List

from sqlalchemy.orm import Session

from interviewer import models
from interviewer.app.api.exceptions.NotFoundException import NotFoundException
from interviewer.app.api.schemas.Interview import Interview
import datetime

from interviewer.app.api.schemas.InterviewState import InterviewState
from interviewer.app.api.schemas.user import User


class InterviewDao:

    def __init__(self, db: Session):
        self.db = db

    def get_interview_by_id(self, interview_id: int) -> Interview:
        interview = (self.db.query(models.InterviewModel)
                     .filter(models.InterviewModel.interview_id == interview_id)
                     .first())
        if not interview:
            raise NotFoundException("Interview not found")
        return interview.to_interview()

    def get_all_interviews_for_user(self, user: User) -> List[Interview]:
        interview_models = (self.db.query(models.InterviewModel)
                     .filter(models.InterviewModel.user_id == user.user_id)
                     .to_list())

        interviews = []
        for model in interview_models:
            interviews.append(model.to_interview())
        return interviews

    def get_all_finished_interviews(self) -> List[Interview]:
        interview_models = (self.db.query(models.InterviewModel)
                     .filter(models.InterviewModel.state == InterviewState.RUNNING.value)
                     .filter(models.InterviewModel.end_time > datetime.datetime.now())
                     .to_list())

        interviews = []
        for model in interview_models:
            interviews.append(model.to_interview())
        return interviews

    def update_interview_state(self, interview: Interview, new_state: InterviewState) -> Interview:
        interview_model = (self.db.query(models.InterviewModel)
                     .filter(models.InterviewModel.interview_id == interview.interview_id)
                     .first())
        if not interview_model:
            raise NotFoundException("Interview not found")
        interview_model.state = new_state.value
        self.db.commit()
        self.db.refresh(interview_model)
        return interview_model.to_interview()


    def create_interview(self, topic: str,
                         user_id: int,
                         number_of_questions: int,
                         number_of_follow_up_questions: int,
                         duration_in_mins: int) -> Interview:
        db_item = models.InterviewModel(topic=topic, user_id=user_id,
                                        end_time=datetime.datetime.now() + datetime.timedelta(minutes=duration_in_mins),
                                        state=InterviewState.RUNNING.value,
                                        number_of_questions=number_of_questions,
                                        number_of_follow_up_questions=number_of_follow_up_questions)
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item.to_interview()

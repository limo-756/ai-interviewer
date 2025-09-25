from typing import List

from sqlalchemy.orm import Session

from interviewer import models
from interviewer.app.api.schemas.AssessmentItem import AssessmentItem
from interviewer.app.api.schemas.user import User


class AssessmentItemDao:

    def __init__(self, db: Session):
        self.db = db

    def get_assessment_item_by_id(self, assessment_item_id: int) -> AssessmentItem:
        assessment_model_item = (self.db.query(models.InterviewModel)
                     .filter(models.AssessmentItemModel.item_id == assessment_item_id)
                     .first())
        return assessment_model_item.to_assessment_item()

    def get_all_assessment_items_for_interview(self, interview_id: int) -> List[User]:
        assessment_model_items = (self.db.query(models.AssessmentItemModel)
                     .filter(models.AssessmentItemModel.interview_id == interview_id)
                     .to_list())

        assessment_items = []
        for model in assessment_model_items:
            assessment_items.append(model.to_interview())
        return assessment_items


    def create_assessment_item(self, interview_id: int,
                               sequence_no: int,
                               question_id: int,
                               question: str) -> AssessmentItem:
        db_item = models.AssessmentItemModel(interview_id=interview_id,
                                             sequence_no=sequence_no,
                                             question_id=question_id,
                                             question=question)
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item.to_assessment_item()

    def update_assessment_item_with_answer(self, item_id: int,
                               answer: str) -> AssessmentItem:
        assessment_model_item = (self.db.query(models.AssessmentItemModel)
                     .filter(models.AssessmentItemModel.item_id == item_id)
                     .first())
        if assessment_model_item:
            assessment_model_item.answer = answer
        self.db.commit()
        self.db.refresh(assessment_model_item)
        return assessment_model_item.to_assessment_item()

    def update_assessment_item_with_evaluation_log_and_score(self, item_id: int,
                               evaluation_log: str,
                               score: int) -> AssessmentItem:
        assessment_model_item = (self.db.query(models.AssessmentItemModel)
                     .filter(models.AssessmentItemModel.item_id == item_id)
                     .first())
        if assessment_model_item:
            assessment_model_item.evaluation_log = evaluation_log
            assessment_model_item.score = score
        self.db.commit()
        self.db.refresh(assessment_model_item)
        return assessment_model_item.to_assessment_item()

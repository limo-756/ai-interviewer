from typing import List, Optional

from sqlalchemy.orm.session import Session

from interviewer import models
from interviewer.app.api.schemas.Question import Question


class QuestionsDao:
    def __init__(self, db: Session):
        self.db = db

    def get_part1_questions_by_topic(self, topic: str) -> List[Question]:
        questions_models = (self.db.query(models.QuestionsModel)
                     .filter(models.QuestionsModel.topic == topic)
                     .filter(models.QuestionsModel.part_no == 1)
                     .to_list())

        questions = []
        for model in questions_models:
            questions.append(model.to_question())
        return questions

    def get_number_of_questions_on_topic(self, topic:str) -> int:
        return (self.db.query(models.QuestionsModel)
                     .filter(models.QuestionsModel.topic == topic)
                     .filter(models.QuestionsModel.part_no == 1)
                     .count())

    def create_question(self, topic: str, question: str, part_no: Optional[int] = 1, question_id: Optional[int] = None) -> Question:
        if question_id is not None:
            db_item = (self.db.query(models.QuestionsModel)
                         .filter(models.QuestionsModel.question_id == question_id)
                         .filter(models.QuestionsModel.part_no == part_no)
                         .first())
            if db_item is not None:
                db_item.question_statement = question
                db_item.topic = topic
            else:
                db_item = models.QuestionsModel(topic=topic, question_statement=question, question_id=question_id, part_no=part_no)
                self.db.add(db_item)
        else:
            db_item = models.QuestionsModel(topic=topic, question_statement=question, part_no=part_no)
            self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item.to_question()

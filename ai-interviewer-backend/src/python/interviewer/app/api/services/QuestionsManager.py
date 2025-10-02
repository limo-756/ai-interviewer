import random
from typing import List

from interviewer.app.api.dao.assessment_item_dao import AssessmentItemDao
from interviewer.app.api.dao.question_dao import QuestionsDao
from interviewer.app.api.schemas.AssessmentItem import AssessmentItem
from interviewer.app.api.schemas.Interview import Interview
from interviewer.app.api.schemas.Question import Question


class QuestionsManager:
    def __init__(self,
                 questions_dao: QuestionsDao,
                 assessment_item_dao: AssessmentItemDao):
        self.questions_dao = questions_dao
        self.assessment_item_dao = assessment_item_dao

    def assign_questions_for_interview(self, interview: Interview,
                                       number_of_questions: int) -> None:
        topic_name = self._resolve_topic_name(interview.topic)

        if self._should_create_new_questions(topic_name):
            self._generate_new_questions_for_topic(topic_name)

        questions = self._select_questions(interview, number_of_questions)
        for index, question in enumerate(questions):
            self.assessment_item_dao.create_assessment_item(interview.interview_id,
                                                       index + 1,
                                                       1,
                                                       question.question_id,
                                                       question.question_statement)


    def _resolve_topic_name(self, topic: str) -> str:
        return topic

    def _should_create_new_questions(self, topic_name: str) -> bool:
        return False

    def _generate_new_questions_for_topic(self, topic_name: str) -> None:
        return None

    def _select_questions(self, interview: Interview, number_of_questions: int) -> list[
        Question]:
        questions = self.questions_dao.get_questions_by_topic(interview.topic)
        random.shuffle(questions)
        return questions[:number_of_questions]

    def generate_probing_question(self, interview: Interview, question_no: int) -> Question:
        pass

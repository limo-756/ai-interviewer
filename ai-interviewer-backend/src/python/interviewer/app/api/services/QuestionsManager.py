import random

from interviewer.app.api.dao.assessment_item_dao import AssessmentItemDao
from interviewer.app.api.dao.question_dao import QuestionsDao
from interviewer.app.api.schemas.Interview import Interview
from interviewer.app.api.schemas.Question import Question


class QuestionsManager:

    def assign_questions_for_interview(self, interview: Interview,
                                       number_of_questions: int,
                                       questions_dao: QuestionsDao,
                                       assessment_item_dao: AssessmentItemDao) -> None:
        topic_name = self._resolve_topic_name(interview.topic)

        if self._should_create_new_questions(topic_name):
            self._generate_new_questions_for_topic(topic_name)

        questions = self._select_questions(interview, number_of_questions, questions_dao)
        for index, question in enumerate(questions):
            assessment_item_dao.create_assessment_item(interview.interview_id,
                                                       index + 1,
                                                       question.question_id,
                                                       question.question_statement)


    def _resolve_topic_name(self, topic: str) -> str:
        return topic

    def _should_create_new_questions(self, topic_name: str) -> bool:
        return False

    def _generate_new_questions_for_topic(self, topic_name: str) -> None:
        return None

    def _select_questions(self, interview: Interview, number_of_questions: int, questions_dao: QuestionsDao) -> list[
        Question]:
        questions = questions_dao.get_questions_by_topic(interview.topic)
        random.shuffle(questions)
        return questions[:number_of_questions]

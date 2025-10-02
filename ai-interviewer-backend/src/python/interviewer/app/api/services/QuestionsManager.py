import random
from typing import List

from interviewer.app.api.dao.assessment_item_dao import AssessmentItemDao
from interviewer.app.api.dao.interview_dao import InterviewDao
from interviewer.app.api.dao.question_dao import QuestionsDao
from interviewer.app.api.external.LLMService import LLMService
from interviewer.app.api.schemas.AssessmentItem import AssessmentItem
from interviewer.app.api.schemas.Interview import Interview
from interviewer.app.api.schemas.Question import Question


class QuestionsManager:
    def __init__(self,
                 interview_dao: InterviewDao,
                 questions_dao: QuestionsDao,
                 assessment_item_dao: AssessmentItemDao,
                 llm_service: LLMService):
        self.interview_dao = interview_dao
        self.questions_dao = questions_dao
        self.assessment_item_dao = assessment_item_dao
        self.llm_service = llm_service

    def assign_questions_for_interview(self, interview: Interview,
                                       number_of_questions: int) -> None:
        topic_name = self._resolve_topic_name(interview.topic)
        questions = self.questions_dao.get_part1_questions_by_topic(topic_name)
        past_questions = self._get_past_interview_questions(interview)
        questions = self._remove_past_questions(questions, past_questions)
        should_create_new_questions = number_of_questions > len(questions)

        if should_create_new_questions:
            questions.extend(self._generate_new_questions_for_topic(topic_name, len(questions) - number_of_questions))

        questions = self._select_questions(questions, number_of_questions)
        for index, question in enumerate(questions):
            self.assessment_item_dao.create_assessment_item(interview.interview_id,
                                                       index + 1,
                                                       1,
                                                       question.question_id,
                                                       question.question_statement)


    def _resolve_topic_name(self, topic: str) -> str:
        return topic

    def _get_past_interview_questions(self, interview: Interview) -> List[AssessmentItem]:
        past_interviews = self.interview_dao.get_all_past_interviews_for_user(interview.user_id)
        past_questions = []
        for past_interview in past_interviews:
            if past_interview.topic == interview.topic:
                past_questions.extend(
                    self.assessment_item_dao.get_all_part1_assessment_items_for_interview(past_interview.interview_id))
        return past_questions

    def _remove_past_questions(self, questions: List[Question], past_questions: List[AssessmentItem]) -> List[Question]:
        past_question_set = set()
        for question in past_questions:
            past_question_set.add(question.question_id)

        filtered_questions = []
        for question in questions:
            if question.question_id not in past_question_set:
                filtered_questions.append(question)
        return filtered_questions

    def _generate_new_questions_for_topic(self, topic_name: str, number_of_questions_to_create: int) -> List[Question]:
        question = self.llm_service.generate_questions(topic_name, max(number_of_questions_to_create, 10))
        new_questions = []
        for index, question in enumerate(question):
            new_questions.append(self.questions_dao.create_question(
                topic=topic_name,
                question=question,
                part_no=1,
                question_id=None
            ))
        return new_questions

    def _select_questions(self, questions: List[Question], number_of_questions: int) -> List[Question]:
        random.shuffle(questions)
        return questions[:number_of_questions]

    def generate_probing_question(self, interview: Interview, question_no: int) -> Question:
        assessment_items = self.assessment_item_dao.get_all_assessment_items_for_question(interview.interview_id,
                                                                        question_no)
        questions = [item.question for item in assessment_items]
        answers = [item.answer for item in assessment_items]
        new_question = self.llm_service.generate_probing_question(self._resolve_topic_name(interview.topic),
                                                                  questions,
                                                                  answers)
        return self.questions_dao.create_question(
            topic=self._resolve_topic_name(interview.topic),
            question=new_question,
            part_no=len(assessment_items) + 1,
            question_id=None
        )
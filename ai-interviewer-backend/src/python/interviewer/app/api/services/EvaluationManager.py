from concurrent.futures.thread import ThreadPoolExecutor
from time import sleep

from interviewer.app.api.dao.assessment_item_dao import AssessmentItemDao
from interviewer.app.api.dao.interview_dao import InterviewDao
from interviewer.app.api.external.LLMService import LLMService
from interviewer.app.api.schemas.AssessmentItem import AssessmentItem
from interviewer.app.api.schemas.Interview import Interview
from interviewer.app.api.schemas.InterviewState import InterviewState


class EvaluationManager:

    def __init__(self, interview_dao: InterviewDao, assessment_items_dao: AssessmentItemDao, llm: LLMService):
        self.interview_dao = interview_dao
        self.assessment_items_dao = assessment_items_dao
        self.llm = llm
        self.interview_evaluation_tracker = {}
        self.finished_interview_processor = ThreadPoolExecutor(max_workers=1)
        self.question_evaluator = ThreadPoolExecutor(max_workers=5)
        self.evaluation_status_updator = ThreadPoolExecutor(max_workers=1)

    class EValuationTask:
        def __init__(self, assessment_item: AssessmentItem):
            self.assessment_item = assessment_item

    def process_finished_interviews(self):
        while True:
            interviews = self.interview_dao.get_all_interviews_for_user()

            for interview in interviews:
                print(f"Started evaluating interview {interview.interview_id}")
                self.interview_dao.update_interview_state(interview, InterviewState.FINISHED)
                assessment_items = self.assessment_items_dao.get_all_part1_assessment_items_for_interview(
                    interview.interview_id)
                number_of_questions_answered = sum(filter(lambda item: item.is_attempted(), assessment_items))
                self.interview_evaluation_tracker[interview.interview_id] = number_of_questions_answered
                for item in assessment_items:
                    if item.is_attempted():
                        self.question_evaluator.submit(self.evaluate_question, self.EValuationTask(item))
                print(f"Submitted all questions for evaluation for interview {interview.interview_id}")
            sleep(1)

    def evaluate_question(self, task: EValuationTask):
        print(f"Evaluating question {task.assessment_item.item_id}")
        evaluation_log, score = self.llm.evaluate_question(task.assessment_item.question, task.assessment_item.answer)
        self.assessment_items_dao.update_assessment_item_with_evaluation_log_and_score(task.assessment_item.item_id,
                                                                                         task.assessment_item.evaluation_log,
                                                                                         score)
        self.interview_evaluation_tracker[task.assessment_item.interview_id] -= 1
        print(f"Question {task.assessment_item.item_id} evaluated")

    def update_evaluation_status(self, interview: Interview):
        while True:
            if self.interview_evaluation_tracker.get(interview.interview_id) <= 0:
                self.interview_dao.update_interview_state(interview, InterviewState.EVALUATED)
                print(f"Interview {interview.interview_id} evaluation completed")
                return
            sleep(1)

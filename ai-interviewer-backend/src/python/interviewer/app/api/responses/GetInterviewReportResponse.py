from typing import List


class GetInterviewReportResponse:
    class InterviewReport:
        def __init__(self, question_number: int, question_statement: str, answer: str, evaluation_logs: str, score: int, max_score: int):
            self.question_number = question_number
            self.question_statement = question_statement
            self.answer = answer
            self.evaluation_logs = evaluation_logs
            self.score = score
            self.max_score = max_score

    total_score: int
    total_marks: int
    status: str
    report: List[InterviewReport]

    def __init__(self, total_score: int, total_marks: int, status: str, report: List[InterviewReport]):
        self.total_score = total_score
        self.total_marks = total_marks
        self.status = status
        self.report = report
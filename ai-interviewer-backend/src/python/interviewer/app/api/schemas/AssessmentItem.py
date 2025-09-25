class AssessmentItem:
    item_id: int
    interview_id: int
    sequence_no: int
    question_id: int
    question: str
    answer: str
    evaluation_log: str
    score: int

    def __init__(self,
                 item_id: int,
                 interview_id: int,
                 sequence_no: int,
                 question_id: int,
                 question: str,
                 answer: str,
                 evaluation_log: str,
                 score: int
    ):
        self.item_id = item_id
        self.interview_id = interview_id
        self.sequence_no = sequence_no
        self.question_id = question_id
        self.question = question
        self.answer = answer
        self.evaluation_log = evaluation_log
        self.score = score

    def is_evaluation_complete(self) -> bool:
        return self.answer is not None and self.score is not None


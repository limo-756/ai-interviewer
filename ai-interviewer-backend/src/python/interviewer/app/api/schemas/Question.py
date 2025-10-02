class Question:
    question_id: int
    part_no: int
    question_statement: str
    topic: str

    def __init__(self, question_id: int, part_no: int, question_statement: str, topic: str):
        self.question_id = question_id
        self.part_no = part_no
        self.question_statement = question_statement
        self.topic = topic

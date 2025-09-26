class Question:
    question_id: int
    question_statement: str
    topic: str

    def __init__(self, question_id: int, question_statement: str, topic: str):
        self.question_id = question_id
        self.question_statement = question_statement
        self.topic = topic

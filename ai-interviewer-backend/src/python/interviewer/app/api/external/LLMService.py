from typing import List

from openai import OpenAI

class LLMService:
    def __init__(self):
        self.client = OpenAI()
        key = "XXXXX"

    def evaluate_question(self, question, answer):
        response = self.client.responses.create(
            model="gpt-5",
            input="Write a short bedtime story about a unicorn."
        )

    def evaluate_question_with_parts(self, questions: List[str], answer: List[str]):
        response = self.client.responses.create(
            model="gpt-5",
            input="Write a short bedtime story about a unicorn."
        )

    def generate_questions(self, topic: str, number_of_questions: int = 10) -> List[str]:
        return "response"

    def generate_probing_question(self, topic: str, questions: List[str], answer: List[str]) -> str:
        return "response"

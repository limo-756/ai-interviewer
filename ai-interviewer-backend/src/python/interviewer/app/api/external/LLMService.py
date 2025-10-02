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

    def generate_response(self, prompt):
        return "response"

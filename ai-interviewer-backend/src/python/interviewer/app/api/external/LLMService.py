from openai import OpenAI

class LLMService:
    def __init__(self):
        client = OpenAI()
        key = "XXXXX"

    def evaluate_question(self, question, answer):
        response = client.responses.create(
            model="gpt-5",
            input="Write a short bedtime story about a unicorn."
        )

    def generate_response(self, prompt):
        return "response"

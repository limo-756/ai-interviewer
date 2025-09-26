from interviewer.app.api.requests.BaseRequest import BaseRequest


class StartInterviewRequest(BaseRequest):
    topic: str
    resumeFile: str

    def validate(self):
        if not self.topic or len(self.topic.strip()) == 0:
            raise ValueError("Topic is invalid")

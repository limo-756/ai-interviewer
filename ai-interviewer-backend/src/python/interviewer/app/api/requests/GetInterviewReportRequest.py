class GetInterviewReportRequest:
    interview_id: int

    def validate(self):
        if self.interview_id < 1:
            raise ValueError("Interview id must be greater than 0")
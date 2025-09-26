from interviewer.app.api.requests.BaseRequest import BaseRequest
from interviewer.app.api.utils.validationUtils import is_email_valid, is_password_valid


class LoginRequest(BaseRequest):
    email: str
    password: str

    def validate(self):
        if not is_email_valid(self.email):
            raise ValueError("Email is invalid")

        if not is_password_valid(self.password):
            raise ValueError("Password is invalid")

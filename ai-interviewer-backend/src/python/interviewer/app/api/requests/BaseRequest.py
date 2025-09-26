from abc import abstractmethod


class BaseRequest:
    def __post_init__(self):
        self.validate()

    @abstractmethod
    def validate(self):
        raise ValueError("Request validation failed")

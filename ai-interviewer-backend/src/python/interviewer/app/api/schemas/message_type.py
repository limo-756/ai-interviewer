from enum import Enum


class MessageType(Enum):
    INTRO = "INTRO"
    FEEDBACK = "FEEDBACK"
    QUESTION = "QUESTION"
    ANSWER = "ANSWER"
from interviewer.app.api.schemas.message_type import MessageType
from interviewer.app.api.schemas.participant_type import ParticipantType


class InterviewChat:
    chat_id: int
    interview_id: int
    sequence_no: int
    participant_type: ParticipantType
    message: str
    message_type: MessageType

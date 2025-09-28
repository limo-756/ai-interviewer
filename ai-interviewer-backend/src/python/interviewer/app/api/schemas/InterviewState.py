import enum


class InterviewState(enum.Enum):
    SCHEDULED = "SCHEDULED"
    RUNNING = "RUNNING"
    FINISHED = "FINISHED"
    EVALUATED = "EVALUATED"

    def from_str(cls, state: str):
        switcher = {
            "SCHEDULED": cls.SCHEDULED,
            "RUNNING": cls.RUNNING,
            "FINISHED": cls.FINISHED,
            "EVALUATED": cls.EVALUATED,
        }
        return switcher.get(state, cls.SCHEDULED)

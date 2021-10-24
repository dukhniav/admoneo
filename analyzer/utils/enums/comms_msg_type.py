from enum import Enum


class CommsMsgType(Enum):
    STATUS = 'status'
    WARNING = 'warning'
    STARTUP = 'startup'

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value

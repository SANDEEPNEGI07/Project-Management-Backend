import enum


class OrganizationStatus(str, enum.Enum):
    ACTIVE = "active"
    ARCHIEVED = "archieved"


class ProjectStatus(str, enum.Enum):
    PLANNED = "planned"
    IN_PROCESS = "in-process"
    COMPLETED = "completed"


class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in-progress"
    DONE = "done"


class TaskPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

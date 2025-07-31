from enum import Enum

class RoleEnum(Enum):
    ADMIN = "admin"
    USER = "user"

class SpotEnum(Enum):
    AVAILABLE = 'available'
    OCCUPIED = 'occupied'
    RESERVED = 'reserved'
    OUT_OF_SERVICE = 'out_of_service'

class ReservationStatusEnum(Enum):
    ACTIVE = 'active'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'

class ReminderEnum(Enum):
    DAILY = 'daily'
    MONTHLY = 'monthly'

class ExportStatusEnum(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field

from app.utils import now

class ValidatorLog(SQLModel, table=True):
    __tablename__ = "validator_log"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    request_id: UUID = Field(foreign_key="request_log.id", nullable=False)
    input: str
    output: str
    error: str
    inserted_at: datetime = Field(default_factory=now, nullable=False)
    updated_at: datetime = Field(default_factory=now, nullable=False)

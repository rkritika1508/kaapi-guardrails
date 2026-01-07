
from sqlmodel import Session
from uuid import UUID, uuid4

from app.models.request import RequestLog, RequestLogCreate, RequestStatus

class RequestLogCrud:
    def __init__(self, session: Session):
        self.session = session

    def create(self, request_id: UUID):
        create_request_log = RequestLog(
            request_id=request_id,
            response_id=uuid4(),
            status=RequestStatus.SUCCESS,
            request_text="hello",
            response_text="bye"
        )
        self.session.add(create_request_log)
        self.session.commit()
        self.session.refresh(create_request_log)
        return create_request_log

    def update(self, request_log_id: UUID, response_id: UUID, output_text: str):
        pass


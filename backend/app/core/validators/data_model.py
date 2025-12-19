from pydantic import BaseModel

class ValidatorDataItem(BaseModel):
    type: str
    version: str
    source: str

class ValidatorData(BaseModel):
    validators: list[ValidatorDataItem] 
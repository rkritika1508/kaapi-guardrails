from guardrails import OnFailAction
from sqlmodel import SQLModel
from typing import Any, Callable, ClassVar, Optional, Type

class BaseValidatorConfig(SQLModel):
    # override in subclasses
    validator_cls: ClassVar[Type[Any] | None] = None
    on_fail: Optional[Callable] = OnFailAction.FIX

    model_config = {"arbitrary_types_allowed": True}
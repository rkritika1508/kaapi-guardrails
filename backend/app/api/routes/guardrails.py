from fastapi import APIRouter, HTTPException
from guardrails import Guard
from guardrails.utils.validator_utils import get_validator
from app.models.guardrail_config import GuardrailInputRequest, GuardrailOutputRequest
from app.api.deps import AuthDep

router = APIRouter(prefix="/guardrails", tags=["guardrails"])

@router.post("/input/")
async def run_input_guardrails(
    payload: GuardrailInputRequest,
    _: AuthDep,
):
    response_id = "ABC"

    try:
        prepare_validators(payload.validators)
        guard = build_guard(payload.validators)
        result = guard.validate(payload.input)

        if result.validated_output is not None:
            return {
                "response_id": response_id,
                "safe_input": result.validated_output,
            }

        return {
            "response_id": response_id,
            "error": {
                "type": "validation_error",
                "action": "reask" if result.failures else "fail",
            },
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "response_id": response_id,
                "error": {
                    "type": "config_error",
                    "reason": str(e),
                },
            },
        )

def prepare_validators(validator_items):
    for v_item in validator_items:
        post_init = getattr(v_item, "post_init", None)
        if post_init:
            post_init()

def build_guard(validator_items):
    validators = []

    for v_item in validator_items:
        params = v_item.model_dump()
        v_type = params.pop("type")

        validator_cls = getattr(v_item, "validator_cls", None)
        if validator_cls:
            validators.append(validator_cls(**params))
        else:
            validators.append(
                get_validator({
                    "type": v_type,
                    **params,
                })
            )

    # 🔴 THIS LINE IS ESSENTIAL
    return Guard().use_many(*validators)

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from guardrails import Guard
from app.models.guardrail_config import GuardrailInputRequest, GuardrailOutputRequest
from app.api.deps import AuthDep
from app.core.api_response import APIResponse

from app.core.validators.registry import (
    ValidatorRegistry,
    load_validator_data
)


router = APIRouter(prefix="/guardrails", tags=["guardrails"])

@router.post("/input/")
async def run_input_guardrails(
    payload: GuardrailInputRequest,
    _: AuthDep,
):
    response_id = "ABC"

    try:
        guard = build_guard(payload.validators)
        result = guard.validate(payload.input)

        if result.validated_output is not None:
            return APIResponse.success_response(
                data={
                    "response_id": response_id,
                    "safe_input": result.validated_output,
                }
            )

        # validation failure → 400
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=APIResponse.failure_response(
                error={
                    "response_id": response_id,
                    "type": "validation_error",
                    "action": "reask" if result.failures else "fail",
                    "failures": [
                        f.failure_message for f in (result.failures or [])
                    ],
                }
            ).model_dump(),
        )

    except Exception as e:
        # config/runtime error → 500
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=APIResponse.failure_response(
                error={
                    "response_id": response_id,
                    "type": "config_error",
                    "reason": str(e),
                }
            ).model_dump(),
        )


@router.post("/output")
async def run_output_guardrails(
    payload: GuardrailOutputRequest,
    _: AuthDep,
):
    response_id = "ABC"

    try:
        guard = build_guard(payload.validators)
        result = guard.validate(payload.output)

        if result.validated_output is not None:
            return APIResponse.success_response(
                data={
                    "response_id": response_id,
                    "safe_output": result.validated_output,
                }
            )

        # validation failure → 400
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=APIResponse.failure_response(
                error={
                    "response_id": response_id,
                    "type": "validation_error",
                    "action": "reask" if result.failures else "fail",
                    "failures": [
                        f.failure_message for f in (result.failures or [])
                    ],
                }
            ).model_dump(),
        )

    except Exception as e:
        # config/runtime error → 500
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=APIResponse.failure_response(
                error={
                    "response_id": response_id,
                    "type": "config_error",
                    "reason": str(e),
                }
            ).model_dump(),
        )

def build_guard(validator_items):
    validators = [v_item.build() for v_item in validator_items]
    return Guard().use_many(*validators)
    # 🔴 THIS LINE IS ESSENTIAL
    return Guard().use_many(*validators)


@router.get("/validator/")
async def get_validators(
    _: AuthDep,
):
    validator_data = load_validator_data()
    validators = validator_data.validators

    output = []
    for validator in validators:
        validator_config = ValidatorRegistry.get(validator.type)
        output.append({"type": validator.type , "config": validator_config.model_json_schema()})
    return {"validators": output}

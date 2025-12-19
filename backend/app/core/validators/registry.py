from pydantic import BaseModel, ValidationError
from pathlib import Path
import json
import logging

from app.models.lexical_slur_safety_validator_config import LexicalSlurSafetyValidatorConfig
from app.models.pii_remover_safety_validator_config import PIIRemoverSafetyValidatorConfig
from app.models.gender_assumption_bias_safety_validator_config import GenderAssumptionBiasSafetyValidatorConfig
from app.core.validators.data_model import ValidatorData

class ValidatorRegistry:
    PII_BAN = "pii_ban"
    ULI_SLUR_LIST = "uli_slur_list"
    BAN_LIST = "ban_list"

    _registry = {
        PII_BAN: PIIRemoverSafetyValidatorConfig,
        ULI_SLUR_LIST: LexicalSlurSafetyValidatorConfig
    }

    @classmethod
    def get(cls, name: str):
        return cls._registry.get(name)


def load_validator_data() -> ValidatorData:
    data_file_path = Path(__file__).parent / "data.json"
    print(data_file_path)
    try: 
        with open(data_file_path, "r") as f:
            json_data = json.load(f)
            print(json_data)
            print(type(json_data))
            return ValidatorData(**json_data)
    except FileNotFoundError:
        logging.error(f"Error: Validator data file not found at {data_file_path}")
        raise
    except json.JSONDecodeError as e:
        logging.error(f"Error: Failed to decode JSON from {data_file_path} : {e}")
        raise
    except ValidationError as e:
        logging.error(f"Error: Unable to validate json fields")
        raise

import json


def validate_json(value: str, field_name: str) -> dict:
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON in {field_name}")


VALID_SCM_TYPES = {"", "git", "hg", "svn", "manual"}


def validate_scm_type(scm_type: str) -> None:
    if scm_type not in VALID_SCM_TYPES:
        raise ValueError(f"Invalid SCM type. Must be one of: {', '.join(VALID_SCM_TYPES)}")


def validate_verbosity(level: int) -> None:
    if level not in range(5):
        raise ValueError("Verbosity must be between 0 and 4")

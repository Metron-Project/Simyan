__all__ = ["BaseModel"]

from pydantic import BaseModel as PydanticModel


class BaseModel(
    PydanticModel,
    populate_by_name=True,
    str_strip_whitespace=True,
    validate_assignment=True,
    revalidate_instances="always",
    extra="ignore",
):
    """Base model for Simyan resources."""

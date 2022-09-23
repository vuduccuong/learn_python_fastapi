#  author = "Vũ Đức Cường"
#  date = 9/22/22, 11:20 PM
from typing import Generic, TypeVar, Optional

from pydantic import Field
from pydantic.generics import GenericModel

T = TypeVar("T")


class IResponseModelBase(GenericModel, Generic[T]):
    success: bool = True
    error_message: Optional[str] = ""
    data: Optional[T] = None
    total: Optional[int] = 0

    class Config:
        allow_population_by_field_name = True

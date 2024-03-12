from typing import Any, Dict, Generic, Optional, Type, TypeVar, Union
from uuid import UUID

from fastapi import HTTPException


ModelType = TypeVar("ModelType")


class DuplicatedEntryError(HTTPException):
    def __init__(self, message):
        super().__init__(status_code=422, detail=message)


class CustomValidationError(HTTPException):
    def __init__(self, message):
        super().__init__(status_code=400, detail=message)


class IdOrSlugNotFoundException(HTTPException, Generic[ModelType]):
    def __init__(
            self,
            model: Type[ModelType],
            obj_key: Optional[Union[UUID, str, int]] = None,
            headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        if obj_key:
            super().__init__(
                status_code=404,
                detail="{model_name} not found by '{obj_key}'".format(model_name=model.__name__, obj_key=obj_key),
                headers=headers,
            )
            return

        super().__init__(
            status_code=404,
            detail="{model_name} not found".format(model_name=model.__name__),
            headers=headers,
        )


class ForbiddenError(HTTPException):
    def __init__(self):
        super().__init__(status_code=403, detail="Forbidden")



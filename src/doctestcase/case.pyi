from typing import Any, ClassVar, Type, TypeVar, Union
from unittest import TestCase

T = TypeVar('T', bound=Type[TestCase])

class DocTestCase(TestCase):
    __doctestcase__: ClassVar['doctestcase']
    def test_docstring(self) -> None: ...

class doctestcase:
    globals: dict[str, Any]
    options: int
    kwargs: dict[str, Any]
    def __init__(
        self,
        globals: dict[str, Any] = ...,
        options: int = ...,
        **kwargs: Any,
    ) -> None: ...
    def __call__(owner: Union[T, type[T]], cls: T) -> Union[T, DocTestCase]: ...

def test_docstring(self: TestCase) -> None: ...

from typing import Any, ClassVar, Iterable, Optional, Tuple, Union
from unittest import TestCase

class DocTestCase(TestCase):
    fails: ClassVar[bool]
    globs: ClassVar[dict[str, Any]]
    opts: ClassVar[int]

    def __init_subclass__(
        cls,
        fails: bool = ...,
        globs: Optional[dict[str, Any]] = ...,
        opts: int = ...,
    ) -> None: ...
    def test0(self) -> None: ...
    @classmethod
    def to_markdown(cls, title_depth: int = ...) -> str: ...
    @classmethod
    def to_rest(cls, title_char: str = ...) -> str: ...
    @classmethod
    def _get_title_body(cls) -> Tuple[Optional[str], Optional[str]]: ...

class ExampleBlock(list[str]): ...

def parse(test: str) -> Iterable[Union[str, ExampleBlock]]: ...

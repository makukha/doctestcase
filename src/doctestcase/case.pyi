from typing import Any, ClassVar, Optional, Tuple
from unittest import TestCase

class DocTestCase(TestCase):
    globs: ClassVar[dict[str, Any]]
    opts: ClassVar[int]

    def __init_subclass__(
        cls,
        globs: Optional[dict[str, Any]] = ...,
        opts: int = ...,
    ) -> None: ...
    def test0(self) -> None: ...
    @classmethod
    def to_markdown(cls, title_depth: int = ...) -> str: ...
    @classmethod
    def to_rest(cls, title_char: str = ...) -> str: ...
    @classmethod
    def _parts(cls) -> Tuple[Optional[str], Optional[str]]: ...

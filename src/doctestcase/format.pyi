from collections.abc import Iterable
from typing import Optional, Tuple, Union

def to_markdown(
    item: Union[object, str, None],
    title_depth: Optional[int] = ...,
    dedent: bool = ...,
) -> str: ...
def to_rest(
    item: Union[object, str, None],
    title_char: Optional[str] = ...,
    dedent: bool = ...,
) -> str: ...

class ExampleBlock(list[str]): ...

def parse_title_body(s: Optional[str], parse_title: bool = ...) -> Tuple[str, str]: ...
def parse_body_items(s: str) -> Iterable[Union[str, ExampleBlock]]: ...

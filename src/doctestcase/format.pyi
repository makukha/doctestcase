from collections.abc import Iterable
from typing import Optional, Tuple, Union

Item = Union[object, str, None]

def get_title(item: Item) -> str: ...
def get_body(item: Item, parse_title: bool = ..., dedent: bool = ...) -> str: ...
def to_markdown(
    item: Item,
    title_depth: Optional[int] = ...,
    dedent: bool = ...,
) -> str: ...
def to_rest(
    item: Item,
    title_char: Optional[str] = ...,
    dedent: bool = ...,
) -> str: ...

class ExampleBlock(list[str]): ...

def parse_title_body(
    doc: Optional[str],
    parse_title: bool = ...,
) -> Tuple[str, str]: ...
def parse_body_items(body: str) -> Iterable[Union[str, ExampleBlock]]: ...

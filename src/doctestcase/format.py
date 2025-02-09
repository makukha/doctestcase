import re


RX_DOCSTRING = re.compile(
    r"""
    (?P<title>.+?)
    ( (?:\n[ \t]*$)+ \n (?P<body>.*?) )?
    """,
    flags=re.DOTALL | re.MULTILINE | re.VERBOSE,
)
RX_EXAMPLE_BLOCK = re.compile(
    r"""
    # Example block consists of a PS1 line followed by non-blank line
    #   or a series of blank lines followed by PS1 line.
    ^(?= [ ]* >>> )  # starts with PS1 line
    (?:
       [ ]* >>> .*                       $  # PS1 line
      |\n (?![ ]*$) .+                   $  # non-blank line
      |(?: \n [ ]* $)+ (?= \n [ ]* >>> ) $  # blank lines followed by PS1 line
    )*
    \n
    """,
    flags=re.MULTILINE | re.VERBOSE,
)


def to_markdown(item, title_depth=2):
    """
    Convert docstring to `Markdown <https://www.markdownguide.org>`_.

    The first block of non-blank lines up to first blank line represents test case
    title. It is merged into one line and formatted as section heading. Every doctest
    block is enclosed with fenced code block.

    Args:
        item (`object` | `str` | `None`):
            input to be converted. If ``item`` is `str`, it will be used as input,
            otherwise ``item.__doc__`` will be used. If input is blank string or
            ``None``, empty string is returned.
        title_depth (`int` | `None`):
            heading level for test case title; defaults to ``2``. If ``None``,
            title will not be matched and marked up (will be a part of the body text).

    Returns:
        `str`: Markdown formatted text; may be empty.

    Example:

        For ``SimpleCase`` from `~doctestcase.case.doctestcase` example,

        .. code:: pycon

            >>> from doctestcase import to_markdown
            >>> to_markdown(SimpleCase)

        .. code:: markdown

            ## Title

            Paragraph.

            ```pycon
            >>> X * 100
            'yzyz...'
            ```

            Another paragraph.

            ```pycon
            >>> None
            >>> True
            True
            ```
    """
    if item is None:
        return ''
    item = item if isinstance(item, str) else item.__doc__
    parse_title = title_depth is not None

    title, body = parse_title_body(item, parse_title=parse_title)
    if (title, body) == (None, None):
        return ''

    chunks = []
    if parse_title:
        chunks.append('{} {}\n'.format('#' * title_depth, title))

    if body:
        chunks.append('\n')
        for item in parse_body_items(body):
            if isinstance(item, ExampleBlock):
                chunks.extend(('```pycon\n', item, '```\n'))
            else:
                chunks.append(item)

    return ''.join(chunks)


def to_rest(item, title_char='-'):
    """
    Convert docstring to
    `reStructuredText <https://www.sphinx-doc.org/en/master/usage/restructuredtext>`_.

    The first block of non-blank lines up to first blank line represents test case
    title. It is merged into one line and formatted as section heading. Every doctest
    block is enclosed with fenced code block.

    Args:
        item (`object` | `str` | `None`):
            input to be converted. If ``item`` is `str`, it will be used as input,
            otherwise ``item.__doc__`` will be used. If input is blank string or
            ``None``, empty string is returned.
        title_char (`str` | `None`):
            heading underline character for test case title; defaults to ``'-'``.
            If ``None``, title will not be matched and marked up (will be a part
            of the body text).

    Returns:
        `str`: reST formatted text; may be empty.

    Example:

        For ``SimpleCase`` from `~doctestcase.case.doctestcase` example,

        .. code:: pycon

            >>> from doctestcase import to_rest
            >>> to_rest(SimpleCase)

        .. code:: restructuredtext

            Title
            -----

            Paragraph.

            >>> X * 100
            'yzyz...'

            Another paragraph.

            >>> None
            >>> True
            True
    """
    if item is None:
        return ''
    item = item if isinstance(item, str) else item.__doc__
    parse_title = title_char is not None

    title, body = parse_title_body(item, parse_title=parse_title)
    if (title, body) == (None, None):
        return ''

    chunks = []
    if parse_title:
        chunks.append('{}\n{}\n'.format(title, title_char * max(3, len(title))))

    if body:
        chunks.extend(('\n', body))

    return ''.join(chunks)


# helpers


class ExampleBlock(str):
    """Internal marker type to represent lines of block of examples"""


def parse_title_body(s, parse_title=True):
    doc = (s or '').strip()
    if not doc:
        return None, None

    if parse_title:
        if (match := RX_DOCSTRING.fullmatch(doc)) is None:
            raise RuntimeError('unreachable')  # pragma: nocover
        title = ' '.join((t.strip() for t in match.group('title').splitlines()))
        body = match.group('body')
    else:
        title = None
        body = doc

    body = body.strip().expandtabs()
    if body:
        body += '\n'

    return title, body


def parse_body_items(s):
    charno = 0
    for m in RX_EXAMPLE_BLOCK.finditer(s):
        yield s[charno : m.start()]
        yield ExampleBlock(s[m.start() : m.end()])
        charno = m.end()
    yield s[charno:]

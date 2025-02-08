from doctest import DocTestFinder, DocTestRunner, ELLIPSIS, FAIL_FAST
import re
from unittest import TestCase


_R_BLANK = r'\n[ \t]*$'
_RX_DOCSTRING = re.compile(
    rf"""
    (?P<title>.+?)
    ((?:{_R_BLANK})+\n(?P<body>.*?))?
    """,
    flags=re.DOTALL | re.MULTILINE | re.VERBOSE,
)


class DocTestCase(TestCase):
    """
    Base class for user test cases.

    When inherited from this class, user test case class should have docstring with
    one or more doctests. The first block of non-blank lines up to first
    blank line will be treated as doc title when formatted with ``to_markdown()`` or
    ``to_rest()``.

    The class can also be given optional arguments.

    Args:
        fail (bool):
            test case is expected to fail; defaults to ``False``.
        globs (dict[str, Any]):
            dictionary of globals added to doctest global namespace, passed to
            :py:meth:`doctest.DocTestFinder.find`.
        opts (int):
            `doctest` ``optionflags``, passed to `doctest.DocTestRunner` defaults to
            ``ELLIPSIS | FAIL_FAST``.

    >>> class CustomTest(DocTestCase, globs={'x': 'yz'}, opts=ELLIPSIS):
    ...     '''Title
    ...
    ...     >>> x * 100
    ...     'yz...'
    ...     '''

    See also examples in :ref:`usage` section.
    """

    __test__ = False  # don't run tests on this abstract base class

    def __init_subclass__(cls, fails=False, globs=None, opts=ELLIPSIS | FAIL_FAST):
        cls.__test__ = True
        cls.fails = fails
        cls.globs = globs or {}
        cls.opts = opts

    def test0(self):
        finder = DocTestFinder(recurse=False)
        runner = DocTestRunner(optionflags=self.opts)
        if getattr(self, '__doc__', ''):
            name = self.__class__.__name__
            for test in finder.find(self.__doc__, name, globs=self.globs):
                ret = runner.run(test)
                self.assertEqual(self.fails, ret.failed)

    @classmethod
    def to_markdown(cls, title_depth=1):
        """
        Convert docstring to `Markdown <https://www.markdownguide.org>`_ formatted text.

        Args:
            title_depth (int):
                heading level for test case title; defaults to ``1``.

        Returns:
            str: Markdown formatted text; may be empty.

        The first block of non-blank lines up to first blank line represents test case
        title. It is merged into one line and formatted as section heading.

        Every doctest block is enclosed with fenced code block

        .. code:: markdown

            ```pycon
            >>> ...
            ```

        If there is no docstring, empty string is returned.

        For the example above,

        >>> CustomTest.to_markdown(title_depth=2)

        .. code:: markdown

            ## Title

            ```pycon
            >>> x * 100
            'yz...'
            ```
        """
        title, body = cls._get_title_body()
        if not title:
            return ''

        # format title
        chunks = ['{} {}\n'.format('#' * title_depth, title)]

        # format body
        if body:
            chunks.append('\n')
            for item in parse(body):
                if isinstance(item, ExampleBlock):
                    chunks.extend(('```pycon\n', item, '```\n'))
                else:
                    chunks.append(item)

        return ''.join(chunks)

    @classmethod
    def to_rest(cls, title_char='-'):
        """
        Convert docstring to
        `reStructuredText <https://www.sphinx-doc.org/en/master/usage/restructuredtext>`_
        formatted text.

        Args:
            title_depth (int):
                heading level for test case title; defaults to ``1``.

        Returns:
            str: Markdown formatted text; may be empty.

        The first block of non-blank lines up to first blank line represents test case
        title. It is merged into one line and formatted as section heading.

        Every doctest block remains unmodified (a valid reST).

        If there is no docstring, empty string is returned.

        For the example above,

        >>> CustomTest.to_rest(title_char='=')

        .. code:: restructuredtext

            Title
            =====

            >>> x * 100
            'yz...'
        """
        title, body = cls._get_title_body()
        if not title:
            return ''

        # format title
        chunks = ['{}\n{}\n'.format(title, title_char * max(3, len(title)))]

        # append body
        if body:
            chunks.extend(('\n', body))

        return ''.join(chunks)

    @classmethod
    def _get_title_body(cls):
        # check missing or empty docstring
        doc = (cls.__doc__ or '').strip()
        if not doc:
            return None, None
        # parse title and body
        if (match := _RX_DOCSTRING.fullmatch(doc)) is None:
            raise RuntimeError('unreachable')  # pragma: nocover

        title = ' '.join((ln.strip() for ln in match.group('title').splitlines()))
        body = match.group('body')
        return title, body.strip() + '\n' if body else body


# helpers


class ExampleBlock(str):
    """Marker type to represent lines of block of examples"""


_EXBLOCK_RE = re.compile(
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


def parse(text):
    string = (text if text.endswith('\n') else text + '\n').expandtabs()
    charno = 0
    for m in _EXBLOCK_RE.finditer(string):
        yield string[charno : m.start()]
        yield ExampleBlock(string[m.start() : m.end()])
        charno = m.end()
    yield string[charno:]

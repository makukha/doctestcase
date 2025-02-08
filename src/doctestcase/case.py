from doctest import (
    DocTestFinder,
    DocTestParser,
    DocTestRunner,
    ELLIPSIS,
    Example,
    FAIL_FAST,
)
from itertools import chain
import re
from typing import Any, ClassVar
from unittest import TestCase


_RX_DOCSTRING = re.compile(r'^(?P<title>.+?)(?:\n\n+(?P<body>.*?))?$', re.DOTALL)


class DocTestCase(TestCase):
    """
    Base class for user test cases.

    When inherited from this class, user test case class should have docstring with
    one or more doctests. The first block of non-blank lines up to first
    blank line will be treated as doc title when formatted with ``to_markdown()`` or
    ``to_rest()``.

    The class can also be given optional arguments.

    Args:
        globs (dict[str, Any]):
            dictionary of globals added to doctest global namespace, passed to
            :py:meth:`doctest.DocTestFinder.find`.
        opts (int):
            `doctest` ``optionflags``, passed to `doctest.DocTestRunner` defaults to
            ``ELLIPSIS | FAIL_FAST``.

    >>> class CustomTest(DocTestCase, globs={'x': 'yz'}, opts=doctest.ELLIPSIS):
    ...     '''Title
    ...
    ...     >>> x * 100
    ...     'yz...'
    ...     '''

    See also examples in :ref:`usage` section.
    """

    globs: ClassVar[dict[str, Any]]
    opts: ClassVar[int]

    def __init_subclass__(cls, globs=None, opts=ELLIPSIS | FAIL_FAST):
        cls.globs = globs or {}
        cls.opts = opts

    def test0(self):
        finder = DocTestFinder(recurse=False)
        runner = DocTestRunner(optionflags=self.opts)
        if getattr(self, '__doc__', ''):
            name = self.__class__.__name__
            for test in finder.find(self.__doc__, name, globs=self.globs):
                ret = runner.run(test)
                self.assertFalse(ret.failed)

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
        title, body = cls._parts()
        if not title:
            return ''

        # format title
        title = ' '.join((line.strip() for line in title.splitlines()))
        lines = ['{} {}\n'.format('#' * title_depth, title)]

        # format body
        if body:
            block = []
            for item in chain(DocTestParser().parse(body), ('')):  # '' closes block
                if isinstance(item, Example):
                    if not block:  # open doctest block
                        block.append('```pycon\n')
                    block.append(item.source)
                else:
                    if block:  # close doctest block if any
                        block.append(item)
                        lines.extend(block)
                        lines.append('```\n')
                        block = []
                    lines.append(item)  # append interleaving text

        return ''.join(lines)

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

        >>> CustomTest.to_rest(title_char='~')

        .. code:: restructuredtext

            Title
            ~~~~~

            >>> x * 100
            'yz...'
        """
        title, body = cls._parts()
        if not title:
            return ''

        # format title
        title = ' '.join((line.strip() for line in title.splitlines()))
        lines = ['{}\n{}\n'.format(title, title_char * len(title))]

        # append body
        if body:
            lines.append(body)

        return ''.join(lines)

    @classmethod
    def _parts(cls):
        # check missing or empty docstring
        if cls.__doc__ == DocTestCase.__doc__:
            return None, None
        doc = cls.__doc__.strip() + '\n'
        if not doc:
            return None, None
        # parse title and body
        if (match := _RX_DOCSTRING.match(doc)) is None:
            return None, None
        return match.group('title'), match.group('body')

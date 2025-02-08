from doctest import DocTestFinder, DocTestRunner, ELLIPSIS, FAIL_FAST
from typing import Any, ClassVar
from unittest import TestCase


class DocTestCase(TestCase):
    """
    Base class for user test cases.

    When inherited from this class, user test case class should have docstring with
    one or more doctests. The first block of non-blank lines up to first
    blank line will be treated as doc title when formatted with ``doc_md()`` or
    ``doc_rst()``.

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

    def __init_subclass__(cls, globs: dict[str, Any], opts: int = ELLIPSIS | FAIL_FAST) -> None:
        cls.globs = globs
        cls.opts = opts

    def test0(self) -> None:
        finder = DocTestFinder(recurse=False)
        runner = DocTestRunner(optionflags=self.opts)
        if getattr(self, '__doc__', ''):
            name = self.__class__.__name__
            for test in finder.find(self.__doc__, name, globs=self.globs):
                ret = runner.run(test)
                self.assertFalse(ret.failed)

    @classmethod
    def doc_markdown(cls, title_depth: int = 1) -> str:
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

        >>> CustomTest.doc_markdown(title_depth=2)

        .. code:: markdown

            ## Title

            ```pycon
            >>> x * 100
            'yz...'
            ```
        """
        if cls.__doc__ == DocTestCase.__doc__:
            return ''
        return cls.__doc__


    @classmethod
    def doc_rest(cls, title_char: str = '-') -> str:
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

        >>> CustomTest.doc_rest(title_char='~')

        .. code:: restructuredtext

            Title
            ~~~~~

            >>> x * 100
            'yz...'
        """
        if cls.__doc__ == DocTestCase.__doc__:
            return ''
        return cls.__doc__

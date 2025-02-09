from doctest import DocTestFinder, DocTestRunner


class doctestcase:
    """
    Class decorator that adds docstring doctests evaluation to subclasses of
    `unittest.TestCase`.

    Arguments passed to decorator are stored under decorated class attribute
    ``__doctestcase__``. New test method ``test_docstring``, implementing docstring
    evaluation, is added to the decorated class.

    The decorator can be equally used with and without arguments. If used without
    arguments, default values are used.

    If the decorated class has no docstring or the docstring is blank, it is not
    executed. The decorated class, as a subclass of `unittest.TestCase`, can define
    its own test methods (exept ``test_docstring``) and
    :py:meth:`~unittest.TestCase.setUp` / `~unittest.TestCase.tearDown` fixture
    methods that are executed before or after the docstring.

    Args:
        globals (`dict` | `None`):
            dictionary of globals passed to the doctest; defaults to ``None``
            (no additional globals). If decorated class already has `__doctestcase__`
            attribute, `__doctestcase__.globals` dict is shallow-copied and updated
            with new ``globals``.
        options (`int`):
            `doctest` ``optionflags``, passed to `doctest.DocTestRunner`; defaults to
            no options. If decorated class already has `__doctestcase__` attribute,
            `__doctestcase__.options` value remains unchanged if ``options=0`` and
            is replaced with new ``options`` otherwise.
        kwargs (`dict`):
            additional keyword arguments that will be stored under
            ``__doctestcase__.kwargs`` and available to
            :py:meth:`~unittest.TestCase.setUp`/:py:meth:`~unittest.TestCase.tearDown`
            and other `~unittest.TestCase` methods, e.g. custom tests.
            If decorated class already has `__doctestcase__` attribute,
            `__doctestcase__.kwargs` dict is shallow-copied and updated with new
            ``kwargs``.

    Returns:
        decorated class.

    Example:

        .. code:: python

            from doctest import ELLIPSIS
            from unittest import TestCase

            from doctestcase import doctestcase


            @doctestcase(globals=dict(X='yz'), options=ELLIPSIS)
            class SimpleCase(TestCase):
                \"\"\"
                Title

                Paragraph.

                >>> X * 100
                'yzyz...'

                Another paragraph.

                >>> None
                >>> True
                True
                \"\"\"

    See Also:
         More examples in :ref:`usage` documentation section.
    """
    def __init__(self, globals=None, options=0, **kwargs):
        self.globals = globals or {}
        self.options = options
        self.kwargs = kwargs

    def __call__(self, cls):
        if hasattr(cls, '__doctestcase__'):
            old = cls.__doctestcase__
            if self.globals:
                self.globals = {**old.globals, **self.globals}
            self.options = old.options if self.options == 0 else self.options
            if self.kwargs:
                self.kwargs = {**old.kwargs, **self.kwargs}
        cls.__doctestcase__ = self

        if not hasattr(cls, 'test_docstring'):
            cls.test_docstring = test_docstring

        return cls


def test_docstring(self):
    props = self.__doctestcase__
    finder = DocTestFinder(recurse=False)
    runner = DocTestRunner(optionflags=props.options)
    if getattr(self, '__doc__', ''):
        name = self.__class__.__name__
        for test in finder.find(self.__doc__, name, globs=props.globals):
            ret = runner.run(test)
            self.assertFalse(ret.failed)

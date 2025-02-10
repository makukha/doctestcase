from doctest import DocTestFinder, DocTestRunner


class doctestcase:
    """
    Class decorator that adds docstring doctests evaluation to subclasses of
    `unittest.TestCase`.

    Args:
        globals (`dict` | `None`):
            dictionary of globals passed to the doctest; defaults to ``None``
            (no additional globals). If decorated class already has `__doctestcase__`
            attribute, `__doctestcase__.globals` dict is updated with new ``globals``.
        options (`int`):
            `doctest` ``optionflags``, passed to `doctest.DocTestRunner`; defaults to
            no options. If decorated class already has `__doctestcase__` attribute,
            `__doctestcase__.options` value is updated (OR-ed) with new ``options``.
        kwargs (`dict`):
            additional keyword arguments that will be stored under
            ``__doctestcase__.kwargs`` and available to
            :py:meth:`~unittest.TestCase.setUp`/:py:meth:`~unittest.TestCase.tearDown`
            and other `~unittest.TestCase` methods, e.g. custom tests.
            If decorated class already has `__doctestcase__` attribute,
            `__doctestcase__.kwargs` dict is updated with new ``kwargs``.

    Arguments passed to decorator are stored under decorated class attribute
    ``__doctestcase__``. New test method ``test_docstring``, implementing docstring
    evaluation, is added to the decorated class.

    The `__doctestcase__` attribute as a copy of original decorator and contains
    shallow copies of original `globals` and `kwargs`.

    If the decorated class has no docstring or the docstring is blank, it is not
    executed. The decorated class, as a subclass of `unittest.TestCase`, can define
    :py:meth:`~unittest.TestCase.setUp` / `~unittest.TestCase.tearDown`
    and its own test methods (exept ``test_docstring``) that are executed
    before or after the docstring.

    The doctestcase object, after being applied to `~unittest.TestCase` class,
    can be further reused to decorate other `~unittest.TestCase` classes. The same
    is true for `__doctestcase__` attribute. On every decoration, a copy of it is
    assigned to `__doctestcase__` attribute of the decorated class.

    When `~unittest.TestCase` is inherited, the inherited class must be decorated
    with `@doctestcase()` again.

    This ensures that `__doctestcase__` attributes of subsequent classes are
    independent, but values of `globals` and `kwargs` remain the same objects.

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
        self.bind = None

    def __call__(self, cls):
        if not hasattr(cls, '__doctestcase__'):
            self._assign(cls)
        elif cls.__doctestcase__.bind is not cls:
            updated = cls.__doctestcase__._copy()
            updated._update(self)
            updated._assign(cls)
        else:
            cls.__doctestcase__._update(self)
        return cls

    def _assign(self, cls):
        cls.__doctestcase__ = self._copy()
        cls.__doctestcase__.bind = cls
        cls.test_docstring = test_docstring

    def _copy(self):
        return self.__class__(
            globals=self.globals.copy(),
            options=self.options,
            **self.kwargs,
        )

    def _update(self, other):
        self.globals |= other.globals
        self.options |= other.options
        self.kwargs |= other.kwargs


def test_docstring(self):
    if self.__doctestcase__.bind is not self.__class__:
        errmsg = 'Class {}, inherited from {}, must be decorated'.format(
            self.__class__.__name__, self.__doctestcase__.bind.__name__,
        )
        raise ValueError(errmsg)

    props = self.__doctestcase__
    finder = DocTestFinder(recurse=False)
    runner = DocTestRunner(optionflags=props.options)
    if getattr(self, '__doc__', ''):
        name = self.__class__.__name__
        for test in finder.find(self.__doc__, name, globs=props.globals):
            ret = runner.run(test)
            self.assertFalse(ret.failed)

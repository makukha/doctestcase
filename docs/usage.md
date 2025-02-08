### Parametrized doctest

First, define a parametrized base class:

<!-- docsub: begin -->
<!-- docsub: include tests/usage/param1.txt -->
<!-- docsub: lines after 1 upto -1 -->
````pycon
>>> import doctest
>>> import os
>>> from typing import ClassVar

>>> from doctestcase import DocTestCase

>>> class ChdirTestCase(DocTestCase):
...     # doctest options (optional)
...     optionflags = doctest.ELLIPSIS | doctest.FAIL_FAST
...
...     cwd: ClassVar[str]  # parameter
...
...     def __init_subclass__(cls, cwd: str = '.', **kwargs):
...         super().__init_subclass__(cls, **kwargs)
...         cls.cwd = cwd
...
...     def __init__(self):
...         self.basedir = None
...
...     def setUp(self):
...         super().tearDown()
...         self.basedir = os.getcwd()
...         # setup other test case resources
...
...     def tearDown(self):
...         # teardown other test case resources
...         os.chdir(self.basedir)
...         self.basedir = os.getcwd()
...         self.basedir = None
````
<!-- docsub: end -->

Now we can define test case parametrized with `cwd`:

<!-- docsub: begin -->
<!-- docsub: include tests/usage/param2.txt -->
<!-- docsub: lines after 1 upto -1 -->
````pycon
>>> class T1(ChdirTestCase, cwd='..'):
...     """Use case title
...
...     Optional paragraphs describing the use case.
...
...     >>> # here goes the doctest example
...     >>> os.getcwd()
...     ...
...
...     More text.
...
...     Multiple paragraphs.
...
...     >>> # another doctest example
...     >>> True
...     True
...     """
...
...     def test_custom(self):
...         ...
````
<!-- docsub: end -->

Additional test methods, if added, are expected to be called after the docstring (internally, the docstring is executed in method with name `test0` that is always alphabetically first; as a consequence, custom methods cannot be named `test0`, but this should be fine as long as the recommended prefix is `test_`).

As a bonus, we can generate Markdown or reST representation of the docstring above to embed it into library docs.

Markdown:

<!-- docsub: begin -->
<!-- docsub: include tests/usage/param3.txt -->
<!-- docsub: lines after 1 upto -1 -->
````pycon
>>> T1.to_markdown() == """\
... # Use case title
...
... Optional paragraphs describing the use case.
...
... ```pycon
... >>> # here goes the doctest example
... >>> os.getcwd()
... ...
... ```
...
... More text.
...
... Multiple paragraphs.
...
... ```pycon
... >>> # another doctest example
... >>> True
... True
... ```
... """
True
````
<!-- docsub: end -->

reStructuredText:

<!-- docsub: begin -->
<!-- docsub: include tests/usage/param4.txt -->
<!-- docsub: lines after 1 upto -1 -->
````pycon
>>> T1.to_rest() == """\
... Use case title
... --------------
...
... Optional paragraphs describing the use case.
...
... >>> # here goes the doctest example
... >>> os.getcwd()
... ...
...
... More text.
...
... Multiple paragraphs.
...
... >>> # another doctest example
... >>> True
... True
... """
True
````
<!-- docsub: end -->

As of now, only title (merged first lines up to double newline) and doctest formatting is supported. Everything else in the docstring is returned as is.


### Non-parametrized doctest

`DocTestCase` can also be used directly if parametrization is not needed:

<!-- docsub: begin -->
<!-- docsub: include tests/usage/direct1.txt -->
<!-- docsub: lines after 1 upto -1 -->
````pycon
>>> from doctestcase import DocTestCase
>>> class T1(DocTestCase):
...     """
...     Multiline
...     title
...
...     >>> True
...     True
...     """
````
<!-- docsub: end -->

Markdown:

<!-- docsub: begin -->
<!-- docsub: include tests/usage/direct2.txt -->
<!-- docsub: lines after 1 upto -1 -->
````pycon
>>> T1.to_markdown() == """\
... # Multiline title
...
... ```pycon
... >>> True
... True
... ```
... """
True
````
<!-- docsub: end -->

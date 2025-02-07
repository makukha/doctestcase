# Usage


## Parametrized doctest

First, declare a parametrized base class:

```pycon
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
...     def __new__(cls, cwd: str = '.', **kwargs):
...         ret = super().__new__(cls, **kwargs)
...         ret.cwd = cwd
...         return ret
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
```

Now we can declare test cases parametrized with `cwd`:

```pycon
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
...     >>> # another doctest example
...     """
... 
...     def test_custom(self):
...         ...
```

Additional est methods, if added, are expected to be called after the docstring (internally, the docstring is executed in method with name `test0` that is always alphabetically first; as a consequence, custom methods cannot be named `test0`, but this should be fine as long as the recommended prefix is `test_`).

As a bonus, we can generate Markdown or RST representation of the docstring above to embed it into library docs:

````pycon
>>> T1.doc_markdown()
# Use case title

Optional paragraphs describing the use case.

```pycon
>>> # here goes the doctest example
>>> os.getcwd()
...
```
     
More text.

```pycon
>>> # another doctest example
```
````

````pycon
>>> T1.doc_rst()
Use case title
==============

Optional paragraphs describing the use case.

>>> # here goes the doctest example
>>> os.getcwd()
...
     
More text.

>>> # another doctest example
````

As of now, only title line and doctest formatting is supported. Everything else in the docstring is returned as is.


## Non-parametrized doctest

The `DocTestCase` can also be used directly if parametrization is not needed:

```pycon
>>> from doctestcase import DocTestCase
>>> class T1(DocTestCase):
...     """Use case title
...     
...     >>> # the doctest example
...     """
```

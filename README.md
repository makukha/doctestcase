# doctestcase
<!-- docsub: begin -->
<!-- docsub: include docs/desc.md -->
> Evaluate doctests with configurable globals and `setUp`–`tearDown`. Format as Markdown and reST to include in docs.
<!-- docsub: end -->

<!-- docsub: begin -->
<!-- docsub: include docs/badges.md -->
[![license](https://img.shields.io/github/license/makukha/doctestcase.svg)](https://github.com/makukha/doctestcase/blob/main/LICENSE)
[![pypi](https://img.shields.io/pypi/v/doctestcase.svg#v0.1.0)](https://pypi.python.org/pypi/doctestcase)
[![python versions](https://img.shields.io/pypi/pyversions/doctestcase.svg)](https://pypi.org/project/doctestcase)
[![tests](https://raw.githubusercontent.com/makukha/doctestcase/v0.1.0/docs/_static/badge-tests.svg)](https://github.com/makukha/doctestcase)
[![coverage](https://raw.githubusercontent.com/makukha/doctestcase/v0.1.0/docs/_static/badge-coverage.svg)](https://github.com/makukha/doctestcase)
[![tested with multipython](https://img.shields.io/badge/tested_with-multipython-x)](https://github.com/makukha/multipython)
[![uses docsub](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/makukha/docsub/refs/heads/main/docs/badge/v1.json)](https://github.com/makukha/docsub)
[![mypy](https://img.shields.io/badge/type_checked-mypy-%231674b1)](http://mypy.readthedocs.io)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/ruff)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
<!-- docsub: end -->

## Features

<!-- docsub: begin -->
<!-- docsub: include docs/features.md -->
* Evaluate doctests
* Configure doctest globals and `setUp`–`tearDown`
* Relies on `unittest.TestCase`
* Minimalistic decorator-based API
* Format docstring as Markdown and reST to include in docs
* Naturally fits [docsub](https://github.com/makukha/docsub)-based pipeline
* No dependencies
* Checked with mypy
* 100% test coverage
* Tested with Python 2.7+
<!-- docsub: end -->

## Alternatives

<!-- docsub: begin -->
<!-- docsub: include docs/alternatives.md -->
* `doctest.DocTestSuite` allows to run doctests with `unittest`, but individual doctests can't be extended, parametrized, or enclosed with `setUp`–`tearDown`.
<!-- docsub: end -->


## Installation

```shell
$ pip install doctestcase
```

## Use cases

<!-- docsub: begin #readme -->
<!-- docsub: include docs/usage.md -->
* Decorated `TestCase`
* Reuse `__doctestcase__` from other `TestCase`
* Parametrize test case
* Inherit from decorated `TestCase`
* Format docstring as Markdown or reStructuredText
* Integration with [docsub](https://github.com/makukha/docsub)

See [API Reference](https://doctestcase.readthedocs.io/en/latest/api.html) for details.


### Decorated `TestCase`

<!-- docsub: begin -->
<!-- docsub: include tests/usage/simple.py -->
<!-- docsub: lines after 1 upto -1 -->
```python
from doctest import ELLIPSIS
from unittest import TestCase

from doctestcase import doctestcase


@doctestcase(globals={'X': 'yz'}, options=ELLIPSIS)
class SimpleCase(TestCase):
    """
    Title

    Paragraph.

    >>> X * 100
    'yzyz...'

    Another paragraph.

    >>> None
    >>> True
    True
    """

    def test_custom(self):  # called before 'test_docstring'
        self.assertTrue(True)

    def test_other(self):  # called after 'test_docstring'
        self.assertTrue(True)

```
<!-- docsub: end -->

All test methods are called by `unittest` in alphabetic order, including `test_docstring`, added by `@doctestcase`.


### Reuse `__doctestcase__` from other `TestCase`

Extending example above,

<!-- docsub: begin -->
<!-- docsub: include tests/usage/reuse.py -->
<!-- docsub: lines after 1 upto -1 -->
```python
@SimpleCase.__doctestcase__
class AnotherCase(TestCase):
    """
    Title

    >>> X * 100
    'yzyz...'
    """
```
<!-- docsub: end -->

Now `AnotherCase.__doctestcase__` holds shallow copy of `globals`, `kwargs`, and same doctest options, as `SimpleCase`. These copies are independent.


### Inherit from decorated class

Inheriting from another test case decorated with `@doctestcase` allows to reuse and extend `globals` and `kwargs` and override doctest options of the base class.

Extending examples above,

<!-- docsub: begin -->
<!-- docsub: include tests/usage/inherit.py -->
<!-- docsub: lines after 1 upto -1 -->
```python
@doctestcase(globals={'A': 'bc'})
class InheritedCase(SimpleCase):
    """
    Title

    >>> (X + A) * 100
    'yzbcyzbc...'
    """
```
<!-- docsub: end -->

Notice that global variable `A` was added to `globals` defined in `SimpleCase`, and the new class reuses `doctest.ELLIPSIS` option.

For more details on how `doctestcase` properties are updated, check the [API Reference](https://doctestcase.readthedocs.io/en/latest/api.html).


### Parametrize doctest case

First, define base class parametrized with `cwd`:

<!-- docsub: begin -->
<!-- docsub: include tests/usage/param-base.py -->
<!-- docsub: lines after 1 upto -1 -->
````python
from doctest import ELLIPSIS
import os.path
import shutil
import tempfile
from unittest import TestCase, skip

from doctestcase import doctestcase


@skip('base class')
@doctestcase(options=ELLIPSIS, cwd='.')
class ChdirTestCase(TestCase):
    def setUp(self):
        self.temp = tempfile.mkdtemp()
        self.prev = os.getcwd()
        cwd = os.path.join(self.temp, self.__doctestcase__.kwargs['cwd'])
        if not os.path.exists(cwd):
            os.mkdir(cwd)
        os.chdir(cwd)

    def tearDown(self):
        os.chdir(self.prev)
        shutil.rmtree(self.temp)
````
<!-- docsub: end -->

Notice how the base class is skipped from testing.

In this example we use `os.path` module for compatibility with older Python versions only. If you use recent Python versions, use `pathlib` instead.

Now we can define test case parametrized with `cwd`:

<!-- docsub: begin -->
<!-- docsub: include tests/usage/param-child.py -->
<!-- docsub: lines after 1 upto -1 -->
````python
@doctestcase(cwd='subdir')
class Case1(ChdirTestCase):
    """
    >>> import os
    >>> os.getcwd()
    '.../subdir'
    """
````
<!-- docsub: end -->


### Inherit from decorated `TestCase`

Test cases, decorated with `@doctestcase`, can be used as base classes for other test cases. This is useful when inherited classes need to extend or change properties, passed to parent's `@doctestcase`. Parent properties will be copied and updated with values from child class decorator.

For the `SimpleCase` class above,

<!-- docsub: begin -->
<!-- docsub: include tests/usage/inherit.py -->
<!-- docsub: lines after 1 upto -1 -->
````python
@doctestcase(globals={'A': 'bc'})
class InheritedCase(SimpleCase):
    """
    Title

    >>> (X + A) * 100
    'yzbcyzbc...'
    """
````
<!-- docsub: end -->


### Format docstring as Markdown or reStructuredText

For the `SimpleCase` class above,

#### Markdown

```pycon
>>> from doctestcase import to_markdown
>>> to_markdown(SimpleCase)
```
<!-- docsub: begin -->
<!-- docsub: include tests/usage/simple.md -->
<!-- docsub: lines after 1 upto -1 -->
````markdown
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
````
<!-- docsub: end -->

#### reStructuredText

```pycon
>>> from doctestcase import to_rest
>>> to_rest(SimpleCase)
```
<!-- docsub: begin -->
<!-- docsub: include tests/usage/simple.rst -->
<!-- docsub: lines after 1 upto -1 -->
````restructuredtext
Title
-----

Paragraph.

>>> X * 100
'yzyz...'

Another paragraph.

>>> None
>>> True
True
````
<!-- docsub: end -->


### Integration with [docsub](https://github.com/makukha/docsub)

When documenting packages, "Usage" section often includes doctests. It is a good practice to test all documented use cases, so why not adopt test-driven documenting approach and write tests with docs in mind?

1. Write tests with carefully crafted docstrings using doctests.
2. Include generated Markdown or reST in docs.

With [docsub](https://github.com/makukha/docsub), this can be achieved with some minimal configuration.

Just two commands to run tests and update docs:

```shell
$ pytest tests
$ docsub sync -i usage.md
```

#### usage.md

<!-- docsub: begin #usage.md -->
<!-- docsub: include tests/docsub/__result__.md -->
<!-- docsub: lines after 1 upto -1 -->
````markdown
# Usage

<!-- docsub: begin -->
<!-- docsub: x case tests/test_usage.py:UseCase1 -->
## Use Case 1

Long description of the use case.

Usage example in doctest:

```pycon
>>> True
True
```
<!-- docsub: end -->
````
<!-- docsub: end #usage.md -->

#### tests/test_usage.py

<!-- docsub: begin -->
<!-- docsub: include tests/docsub/tests/test_usage.py -->
<!-- docsub: lines after 1 upto -1 -->
````python
from unittest import TestCase

from doctestcase import doctestcase


@doctestcase()
class UseCase1(TestCase):
    """
    Use Case 1

    Long description of the use case.

    Usage example in doctest:

    >>> True
    True
    """
````
<!-- docsub: end -->

#### docsubfile.py

Docsub configuration file declaring project-local x-tension command:

<!-- docsub: begin -->
<!-- docsub: include tests/docsub/docsubfile.py -->
<!-- docsub: lines after 1 upto -1 -->
````python
from docsub import click
from doctestcase import to_markdown
from importloc import Location


@click.group()
def x() -> None:
    pass


@x.command()
@click.argument('case')
def case(case: str) -> None:
    text = to_markdown(Location(case).load(), title_depth=2)
    click.echo(text, nl=False)
````
<!-- docsub: end -->
<!-- docsub: end #readme -->

## See also

* [Project documentation](https://doctestcase.readthedocs.io/en/latest)
* [Project changelog](https://github.com/makukha/doctestcase/tree/main/CHANGELOG.md)

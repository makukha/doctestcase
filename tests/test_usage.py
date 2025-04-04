import unittest
from unittest import TestCase

from doctestcase import doctestcase, to_markdown, to_rest  # noqa: F401 # used in exec


# use case: simple


from tests.usage.simple import SimpleCase


# use case: mock


try:
    from unittest import mock
except ImportError:
    import mock  # type: ignore[no-redef]

with mock.patch.object(unittest, 'mock', mock.MagicMock(wraps=mock), create=True):
    with open('tests/usage/mock.py') as f:
        exec(f.read())


# use case: reuse


with open('tests/usage/reuse.py') as f:
    exec(f.read())


# use case: inherit


with open('tests/usage/inherit.py') as f:
    exec(f.read())


# use case: param


with open('tests/usage/param_base.py') as f:
    exec(f.read())
with open('tests/usage/param_child.py') as f:
    exec(f.read())


# use_case: format


class FormatTest(TestCase):
    def test_markdown(self):
        with open('tests/usage/simple.md') as f:
            expected = f.read()
        self.assertEqual(expected, to_markdown(SimpleCase))

    def test_rest(self):
        with open('tests/usage/simple.rst') as f:
            expected = f.read()
        self.assertEqual(expected, to_rest(SimpleCase))

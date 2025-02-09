from unittest import TestCase

from doctestcase import doctestcase, to_markdown, to_rest  # noqa: F401 # used in exec


# use case: simple
from .usage.simple import SimpleCase

# use case: reuse
exec(open('tests/usage/reuse.py').read())

# use case: inherit
exec(open('tests/usage/inherit.py').read())

# use case: param
exec(open('tests/usage/param-base.py').read())
exec(open('tests/usage/param-child.py').read())

# use_case: format
class FormatTest(TestCase):
    def test_markdown(self):
        expected = open('tests/usage/simple.md').read()
        self.assertEqual(expected, to_markdown(SimpleCase))

    def test_rest(self):
        expected = open('tests/usage/simple.rst').read()
        self.assertEqual(expected, to_rest(SimpleCase))

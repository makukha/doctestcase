from doctestcase import DocTestCase


class MissingDocstring(DocTestCase):
    # pass without docstring

    def test_formatting(self):
        self.assertEqual(self.to_markdown(), '')
        self.assertEqual(self.to_rest(), '')


class EmptyDocstring(DocTestCase):
    """"""  # pass with empty docstring

    def test_formatting(self):
        self.assertEqual(self.to_markdown(), '')
        self.assertEqual(self.to_rest(), '')

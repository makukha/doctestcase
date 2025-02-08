from doctestcase import DocTestCase


class MissingDocstring(DocTestCase):
    # pass without docstring

    def test_formatting(self):
        self.assertEquals(self.to_markdown(), '')
        self.assertEquals(self.to_rest(), '')


class EmptyDocstring(DocTestCase):
    """"""  # pass with empty docstring

    def test_formatting(self):
        self.assertEquals(self.to_markdown(), '')
        self.assertEquals(self.to_rest(), '')

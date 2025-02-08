from doctestcase import DocTestCase


# empty and missing


class MissingDocstring(DocTestCase):
    # pass without docstring

    def test_formatting(self):
        self.assertEqual('', self.to_markdown())
        self.assertEqual('', self.to_rest())


class EmptyDocstring(DocTestCase):
    """"""  # pass with empty docstring

    def test_formatting(self):
        self.assertEqual('', self.to_markdown())
        self.assertEqual('', self.to_rest())


# title


class TitleWithoutTrailingNewline(DocTestCase):
    """
    Title"""

    def test_formatting(self):
        self.assertEqual('# Title\n', self.to_markdown())
        self.assertEqual('Title\n-----\n', self.to_rest())


class TitleWithMultipleTrailingNewlines(DocTestCase):
    """
    Title

    """

    def test_formatting(self):
        self.assertEqual('# Title\n', self.to_markdown())
        self.assertEqual('Title\n-----\n', self.to_rest())


class TitleOnFirstLine(DocTestCase):
    # fmt: off
    """Title
    """
    # fmt: on

    def test_formatting(self):
        self.assertEqual('# Title\n', self.to_markdown())
        self.assertEqual('Title\n-----\n', self.to_rest())


class MultilineTitle(DocTestCase):
    """
    Multiline
    Title
    """

    def test_formatting(self):
        self.assertEqual('# Multiline Title\n', self.to_markdown())
        self.assertEqual('Multiline Title\n---------------\n', self.to_rest())


class ShortTitle(DocTestCase):
    """
    T
    """

    def test_formatting(self):
        self.assertEqual('# T\n', self.to_markdown())
        self.assertEqual('T\n---\n', self.to_rest())


# title with text


class TitleWithTextWithoutTrailingNewline(DocTestCase):
    """
    Title

    Text."""

    def test_formatting(self):
        self.assertEqual('# Title\n\nText.\n', self.to_markdown())
        self.assertEqual('Title\n-----\n\nText.\n', self.to_rest())


class TitleWithTextWithManyTrailingNewlines(DocTestCase):
    """
    Title

    Text.

    """

    def test_formatting(self):
        self.assertEqual('# Title\n\nText.\n', self.to_markdown())
        self.assertEqual('Title\n-----\n\nText.\n', self.to_rest())


class TitleWithManyLinesToText(DocTestCase):
    """
    Title


    Text."""

    def test_formatting(self):
        self.assertEqual('# Title\n\nText.\n', self.to_markdown())
        self.assertEqual('Title\n-----\n\nText.\n', self.to_rest())


class TitleWithSpacesLinesToText(DocTestCase):
    """
    Title

    Text."""

    def test_formatting(self):
        self.assertEqual('# Title\n\nText.\n', self.to_markdown())
        self.assertEqual('Title\n-----\n\nText.\n', self.to_rest())

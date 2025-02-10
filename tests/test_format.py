from unittest import TestCase

from doctestcase import to_markdown, to_rest


class Formatting(TestCase):
    def test_missing(self):
        self.assertEqual('', to_markdown(None))
        self.assertEqual('', to_rest(None))

    def test_empty(self):
        self.assertEqual('', to_markdown(''))
        self.assertEqual('', to_rest(''))

    def test_blank(self):
        self.assertEqual('', to_markdown(' \t\n \n'))
        self.assertEqual('', to_rest(' \t\n \n'))

    # title

    def test_no_title(self):
        self.assertEqual('Title\n', to_markdown('Title', title_depth=None))
        self.assertEqual('Title\n', to_rest('Title', title_char=None))

    def test_title_depth(self):
        for i in range(1, 8):
            expected = '{} Title\n'.format('#' * i)
            self.assertEqual(expected, to_markdown('Title', title_depth=i))

    def test_title_char(self):
        for c in '=-^"':
            expected = 'Title\n{}\n'.format(c * len('Title'))
            self.assertEqual(expected, to_rest('Title', title_char=c))

    def test_title_on_single_line(self):
        t = """Title"""
        self.assertEqual('## Title\n', to_markdown(t))
        self.assertEqual('Title\n-----\n', to_rest(t))

    def test_title_on_first_line(self):
        t = 'Title\n'
        self.assertEqual('## Title\n', to_markdown(t))
        self.assertEqual('Title\n-----\n', to_rest(t))

    def test_title_without_trailing_newline(self):
        t = '\nTitle'
        self.assertEqual('## Title\n', to_markdown(t))
        self.assertEqual('Title\n-----\n', to_rest(t))

    def test_title_with_multiple_trailing_newlines(self):
        t = '\nTitle\n'
        self.assertEqual('## Title\n', to_markdown(t))
        self.assertEqual('Title\n-----\n', to_rest(t))

    def test_multiline_title(self):
        t = '\nMultiline\nTitle\n'
        self.assertEqual('## Multiline Title\n', to_markdown(t))
        self.assertEqual('Multiline Title\n---------------\n', to_rest(t))

    def test_short_line(self):
        t = '\nT\n'
        self.assertEqual('## T\n', to_markdown(t))
        self.assertEqual('T\n---\n', to_rest(t))

    # title with text

    def test_title_with_text_without_trailing_newline(self):
        t = '\nTitle\n\nText.\n'
        self.assertEqual('## Title\n\nText.\n', to_markdown(t))
        self.assertEqual('Title\n-----\n\nText.\n', to_rest(t))

    def test_title_with_text_with_multiple_trailing_newlines(self):
        t = '\nTitle\n\nText.\n\n'
        self.assertEqual('## Title\n\nText.\n', to_markdown(t))
        self.assertEqual('Title\n-----\n\nText.\n', to_rest(t))

    def test_title_with_many_lines_to_text(self):
        t = '\nTitle\n\n\nText.'
        self.assertEqual('## Title\n\nText.\n', to_markdown(t))
        self.assertEqual('Title\n-----\n\nText.\n', to_rest(t))

    def test_title_with_blank_lines_to_text(self):
        t = '\nTitle\n    \nText.'
        self.assertEqual('## Title\n\nText.\n', to_markdown(t))
        self.assertEqual('Title\n-----\n\nText.\n', to_rest(t))

    # doctests

    def test_doctest_with_interleaving_text(self):
        t = '\n>>> None\n\nText.\n\n>>> None\n'
        self.assertEqual(
            '```pycon\n>>> None\n```\n\nText.\n\n```pycon\n>>> None\n```\n',
            to_markdown(t),
        )
        self.assertEqual('>>> None\n\nText.\n\n>>> None\n', to_rest(t))

    def test_doctest_with_blank_lines(self):
        t = '\n>>> None\n    \n>>> None\n'
        self.assertEqual('```pycon\n>>> None\n    \n>>> None\n```\n', to_markdown(t))
        self.assertEqual('>>> None\n    \n>>> None\n', to_rest(t))

    def test_doctest_with_exception(self):
        exc = (
            'Traceback (most recent call last):\n'
            '    ...\n'
            'ZeroDivisionError: division by zero\n'
        )
        t = '\nTitle\n\nText1\n\n>>> 0 / 0\n' + exc + '\nText2\n'
        self.assertEqual(
            '## Title\n\nText1\n\n```pycon\n>>> 0 / 0\n' + exc + '```\n\nText2\n',
            to_markdown(t),
        )
        self.assertEqual(
            'Title\n-----\n\nText1\n\n>>> 0 / 0\n' + exc + '\nText2\n',
            to_rest(t),
        )

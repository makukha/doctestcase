from textwrap import dedent

from doctestcase import DocTestCase


class Multiline(DocTestCase):
    """
    Mul
    Tit

    Te
    xt

    Tex
    t
    """

    def test_formatting(self):
        self.assertEqual('# Mul Tit\n\nTe\nxt\n\nTex\nt\n', self.to_markdown())
        self.assertEqual('Mul Tit\n-------\n\nTe\nxt\n\nTex\nt\n', self.to_rest())


class WithException(DocTestCase):
    """
    Title

    Text1

    >>> 0 / 0
    Traceback (most recent call last):
        ...
    ZeroDivisionError: division by zero

    Text2
    """

    def test_formatting(self):
        exc = dedent("""\
        Traceback (most recent call last):
            ...
        ZeroDivisionError: division by zero
        """)
        doctest = '>>> 0 / 0\n{}'.format(exc)
        self.assertEqual(
            '# Title\n\nText1\n\n```pycon\n{}```\n\nText2\n'.format(doctest),
            self.to_markdown(),
        )
        self.assertEqual(
            'Title\n-----\n\nText1\n\n{}\nText2\n'.format(doctest),
            self.to_rest(),
        )


class MultipleMultiline(DocTestCase):
    """
    T

    T1

    >>> None
    >>> 1
    1

    T2

    >>> 2
    2
    """

    def test_formatting(self):
        self.assertEqual(
            '# T\n'
            '\nT1\n\n```pycon\n>>> None\n>>> 1\n1\n```\n'
            '\nT2\n\n```pycon\n>>> 2\n2\n```\n',
            self.to_markdown(),
        )
        self.assertEqual(
            'T\n---\n\nT1\n\n>>> None\n>>> 1\n1\n\nT2\n\n>>> 2\n2\n',
            self.to_rest(),
        )

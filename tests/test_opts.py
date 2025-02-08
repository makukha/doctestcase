from doctestcase import DocTestCase


class TestNoOpts(DocTestCase, opts=0, fails=True):
    """
    doctest.ELLIPSIS is turned off

    >>> 123
    1...
    """


class TestEllipsis(DocTestCase):
    """
    doctest.ELLIPSIS is turned on by default

    >>> 123
    1...
    """

from doctestcase import DocTestCase


class TestFail(DocTestCase, fails=True):
    """
    >>> True
    False
    """

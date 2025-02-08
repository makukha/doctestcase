from doctestcase import DocTestCase


class TestGlobs(DocTestCase, globs={'x': 'yz'}):
    """
    >>> x
    'yz'
    """

@doctestcase(globals=dict(A='bc'))
class InheritedCase(SimpleCase):
    """
    Title

    >>> (X + A) * 100
    'yzbcyzbc...'
    """

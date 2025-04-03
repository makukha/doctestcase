import time
from unittest import TestCase, mock

from doctestcase import doctestcase


@mock.patch('time.time', mock.MagicMock(return_value=0))
@doctestcase()
class WithPatchedTime(TestCase):
    """
    Mocking modules in doctests and testcase methods

    >>> import time
    >>> time.time()
    0
    """

    def test_method(self):
        self.assertEqual(0, time.time())

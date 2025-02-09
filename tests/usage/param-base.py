from doctest import ELLIPSIS, FAIL_FAST
import os.path
import shutil
import tempfile
from unittest import TestCase, skip

from doctestcase import doctestcase


@skip('base class')
@doctestcase(options=ELLIPSIS | FAIL_FAST, cwd='.')
class ChdirTestCase(TestCase):
    def setUp(self):
        self.temp = tempfile.mkdtemp()
        self.prev = os.getcwd()
        cwd = os.path.join(self.temp, self.__doctestcase__.kwargs['cwd'])
        if not os.path.exists(cwd):
            os.mkdir(cwd)
        os.chdir(cwd)

    def tearDown(self):
        os.chdir(self.prev)
        shutil.rmtree(self.temp)

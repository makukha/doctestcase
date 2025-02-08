import doctest
from pathlib import Path
from unittest import TestCase


def run_doctest_files(test_case, paths):  # type: (TestCase, tuple[str, ...]) -> None
    text = '\n\n'.join((Path(p).read_text() for p in paths))
    finder = doctest.DocTestFinder(recurse=False)
    runner = doctest.DocTestRunner(optionflags=doctest.ELLIPSIS | doctest.FAIL_FAST)
    for test in finder.find(text, test_case.__class__.__name__):
        ret = runner.run(test)
        test_case.assertFalse(ret.failed)


class TestDirect(TestCase):
    def runTest(self):  # type: () -> None
        paths = (
            'tests/usage_direct1.txt',
            'tests/usage_direct2.txt',
        )
        run_doctest_files(self, paths)


class TestParam(TestCase):
    def runTest(self):  # type: () -> None
        paths = (
            'tests/usage_param1.txt',
            'tests/usage_param2.txt',
            'tests/usage_param3.txt',
            'tests/usage_param4.txt',
        )
        run_doctest_files(self, paths)

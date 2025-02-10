from unittest import TestCase  # noqa: F401  # used for typing


def assertIndepend(self, deco1, deco2):
    self.assertIsNot(deco1, deco2)
    self.assertIsNot(deco1.globals, deco2.globals)
    self.assertIsNot(deco1.kwargs, deco2.kwargs)


def assertCopy(self, deco1, deco2):
    self.assertEqual(deco1.globals, deco2.globals)
    self.assertEqual(deco1.options, deco2.options)
    self.assertEqual(deco1.kwargs, deco2.kwargs)


def assertExtended(self, deco1, deco2, deco3):
    # deco1 + deco2 = deco3
    self.assertEqual(deco1.globals | deco2.globals, deco3.globals)
    self.assertEqual(deco1.options | deco2.options, deco3.options)
    self.assertEqual(deco1.kwargs | deco2.kwargs, deco3.kwargs)


def assertError(self, case, errmsg):  # type: (TestCase, type[TestCase], str) -> None
    result = case('test_docstring').run()
    self.assertNotEqual(result, None)
    self.assertIn(errmsg, str(result.errors[0][1]))  # type: ignore


def assertFail(self, case):  # type: (TestCase, type[TestCase]) -> None
    result = case('test_docstring').run()
    self.assertNotEqual(result, None)
    self.assertFalse(result.wasSuccessful())  # type: ignore


def assertPass(self, case):  # type: (TestCase, type[TestCase]) -> None
    result = case('test_docstring').run()
    self.assertNotEqual(result, None)
    self.assertTrue(result.wasSuccessful())  # type: ignore

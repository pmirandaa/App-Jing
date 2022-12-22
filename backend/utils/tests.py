from unittest import TestCase

from utils import is_valid_param, bool_param


class UtilsTest(TestCase):
    def setUp(self):
        pass

    def test_is_valid_param(self):
        assert_true = ['0', '1', 'True', 'False', 'true', 'false', 1, 0,
                       True, False, {}, [], (), {'key': 'val'}, [1, 2, 3], (1, 2, 3)]
        assert_false = [None, '']
        for param in assert_true:
            self.assertTrue(is_valid_param(param))
        for param in assert_false:
            self.assertFalse(is_valid_param(param))

    def test_bool_param(self):
        assert_true = ['1', 1, 'True', 'true', True]
        assert_false = ['0', 0, 'False', 'false', False]
        assert_none = [None, '', {}, [], (), {'key': 'val'}, [
            1, 2, 3], (1, 2, 3)]
        for param in assert_true:
            self.assertTrue(bool_param(param))
        for param in assert_false:
            self.assertFalse(bool_param(param))
        for param in assert_none:
            self.assertIsNone(bool_param(param))

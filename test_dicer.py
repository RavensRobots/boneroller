import dicer
import random
import unittest
from unittest import mock


class TestD(unittest.TestCase):

    def test_success(self):
        n = 6

        random.randint = mock.MagicMock()
        random.randint.return_value = 3

        result = dicer.d(n)

        random.randint.assert_called_once_with(1, n)
        self.assertEqual(3, result)

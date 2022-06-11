
from unittest import TestCase
import unittest
import hashlib
from main import compute_sha256


class Test(TestCase):
	def test_compute_sha256(self):
		sha256_swufe='eb6fd8ddbc39ec5437a4363f6c0fcdfa183254f5d6c2b54378b19dae8437e4fd'
		self.assertEqual(compute_sha256('swufe'), sha256_swufe,'error,not equal')


if __name__ == '__main__':
    unittest.main()

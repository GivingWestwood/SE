
from unittest import TestCase
import unittest
#import hashlib
from main import compute_sha256


class Test(TestCase):
    def test_compute_sha256(self):
        sha256_swufe='090b235e9eb8f197f2dd927937222c570396d971222d9009a9189e2b6cc0a2c1'
        self.assertEqual(compute_sha256('swufe'), sha256_swufe,'not equal')
if __name__ == '__main__':
    unittest.main()

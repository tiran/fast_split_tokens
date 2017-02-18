#!/usr/bin/env python3

from __future__ import print_function

import json
import time
import unittest

from ldap.schema.tokenizer import split_tokens
from fast_split_tokens import fast_split_tokens


class SplitTokensTest(unittest.TestCase):
    testfile = 'testcases.jsonl'
    testcases = None
    maxDiff = None
    loops = 10

    @classmethod
    def setUpClass(cls):
        testcases = []
        with open(cls.testfile) as f:
            for line in f:
                testcases.append(json.loads(line))
        cls.testcases = testcases

    def test_split_tokens(self):
        start = time.time()
        for i in range(self.loops):
            for case, expected in self.testcases:
                result = split_tokens(case, {})
                self.assertEqual(expected, result)
        print(time.time() - start)

    def test_fast_split_tokens(self):
        start = time.time()
        for i in range(self.loops):
            for case, expected in self.testcases:
                result = fast_split_tokens(case, {})
                self.assertEqual(expected, result)
        print(time.time() - start)


if __name__ == '__main__':
    unittest.main()

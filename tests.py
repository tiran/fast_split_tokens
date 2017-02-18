#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function

import json
import time
import unittest

from ldap.schema.tokenizer import split_tokens
from fast_split_tokens import fast_split_tokens


class SplitTokensTest(unittest.TestCase):
    testfile = 'testcases.jsonl'
    testcases = [
        # from t_ldap_schema_tokenizer.py
        (" BLUBBER DI BLUBB ", ["BLUBBER", "DI", "BLUBB"]),
        ("BLUBBER DI BLUBB", ["BLUBBER", "DI", "BLUBB"]),
        ("BLUBBER  DI   BLUBB  ", ["BLUBBER", "DI", "BLUBB"]),
        ("BLUBBER  DI  'BLUBB'   ", ["BLUBBER", "DI", "BLUBB"]),
        ("BLUBBER ( DI ) 'BLUBB'   ", ["BLUBBER", "(", "DI", ")", "BLUBB"]),
        ("BLUBBER(DI)", ["BLUBBER", "(", "DI", ")"]),
        ("BLUBBER ( DI)", ["BLUBBER", "(", "DI", ")"]),
        ("BLUBBER ''", ["BLUBBER", ""]),
        ("( BLUBBER (DI 'BLUBB'))",
         ["(", "BLUBBER", "(", "DI", "BLUBB", ")", ")"]),
        ("BLUBB (DA$BLAH)", ['BLUBB', "(", "DA", "BLAH", ")"]),
        ("BLUBB ( DA $  BLAH )", ['BLUBB', "(", "DA", "BLAH", ")"]),
        ("BLUBB (DA$ BLAH)", ['BLUBB', "(", "DA", "BLAH", ")"]),
        ("BLUBB (DA $BLAH)", ['BLUBB', "(", "DA", "BLAH", ")"]),
        ("BLUBB 'DA$BLAH'", ['BLUBB', "DA$BLAH"]),
        ("BLUBB DI 'BLU B B ER' DA 'BLAH' ",
         ['BLUBB', 'DI', 'BLU B B ER', 'DA', 'BLAH']),
        ("BLUBB DI 'BLU B B ER' DA 'BLAH' LABER",
         ['BLUBB', 'DI', 'BLU B B ER', 'DA', 'BLAH', 'LABER']),
        # more
        ("BLUBB '(DA$BLAH)'", ['BLUBB', "(DA$BLAH)"]),
        ("BLUBB '(DA)'", ['BLUBB', "(DA)"]),
        ("BLUBB '(DA BLAH)'", ['BLUBB', "(DA BLAH)"]),
        ("BLUBB 'BLAH \"DA\" BLUBB'", ['BLUBB', 'BLAH \"DA\" BLUBB']),
        ("BLUBB (()('((DA) BLAH)'))",
         ['BLUBB', "(", "(", ")", "(", "((DA) BLAH)", ")", ")"]),

    ]

    extra_testcases = [
        # tab
        ("BLUBB\t'DA\tBLUB'", ['BLUBB', "DA\tBLUB"]),
        # unicode
        (u"BLUBB 'DÄ BLÜBB'", ['BLUBB', u"DÄ BLÜBB"]),
        # for Oracle
        ("BLUBBER DI 'BLU'BB ER' DA 'BLAH' ",
         ["BLUBBER", "DI", "BLU'BB ER", "DA", "BLAH"]),
        # ("BLUBB DI 'BLU B B ER'MUST 'BLAH' ",
        #  ['BLUBB', 'DI', 'BLU B B ER', 'MUST', 'BLAH'])
    ]

    maxDiff = None
    loops = 1

    @classmethod
    def setUpClass(cls):
        testcases = cls.testcases
        with open(cls.testfile) as f:
            for line in f:
                testcases.append(json.loads(line))

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
            for case, expected in self.testcases + self.extra_testcases:
                result = fast_split_tokens(case, {})
                if expected != result:
                    print(case)
                    self.assertEqual(expected, result)
        print(time.time() - start)


if __name__ == '__main__':
    unittest.main()

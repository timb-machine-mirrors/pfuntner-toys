"""
     Unit tests for jsonhunt command

     To run:
       1) cd to the top level toys directory (test is a subdirectory)
       2) type: python -m unittest -v test.jsonhunt
"""

import re

from unittest import TestCase
from bin.jsonhunt import Jsonhunt

# I thought I would need this to sort the results but the results are predictable - lists always
# come out in a certain order given the same output.  Dictionary items can move around but dictionaries
# can be equal even if their elements don't appear to be in the same order as long as their content (keys,
# values) are the same between the two samples.
#
# def sortByPath(root):
#     assert type(root) == list, "root is not a list"
#     assert all([type(item) == dict for item in root]), "all top-level elements are not dictionaries"
#     for element in ["path", "tree"]:
#         assert all([element in item for item in root]), "all top-level elements to have no `%s` element" % element
#     return sorted(root, key=lambda item: item["path"])

class JsonhuntTest(TestCase):
    def test_keyvalue_comprehensive(self):
        hunter = Jsonhunt(re.compile("^[fF]oo"), re.compile("ba+r"), False)
        root = [
            {
                "foo": "bar",
            },
            {
                "foo": "car",
            },
            {
                "foo": "bar",
                "numbers": [0, 1, 2],
            },
            [
                [
                    [
                        [
                            [
                                {
                                    "Foolish": "baaaaaaaaaaart",
                                },
                            ],
                        ],
                    ],
                ],
            ],
            {
                "afoot": "bar",
            },
            {
                "blah": "None",
            },
        ]
        expected = [
            {
                "path": "/0",
                "tree": {
                    "foo": "bar",
                },
            },
            {
                "path": "/2",
                "tree": {
                    "foo": "bar",
                    "numbers": "<3 element list>",
                },
            },
            {
                "path": "/3/0/0/0/0/0",
                "tree": {
                    "Foolish": "baaaaaaaaaaart",
                },
            },
        ]
        self.assertEqual(expected, hunter.hunt(root))

        """
          Repeat scenario with negate=True
        """
        hunter.negate = True
        expected = [
            {
                "path": "/1",
                "tree": {
                    "foo": "car",
                },
            },
        ]

        self.assertEqual(expected, hunter.hunt(root))

    def test_key_comprehensive(self):
        hunter = Jsonhunt(re.compile("^[fF]oo"), None, False)
        root = [
            {
                "foo": "bar",
            },
            {
                "foo": None,
            },
            {
                "foo": 1,
                "numbers": [0, 1, 2],
            },
            [
                [
                    [
                        [
                            [
                                {
                                    "Foolish": "baaaaaaaaaaart",
                                },
                            ],
                        ],
                    ],
                ],
            ],
            {
                "afoot": "bar",
            },
            {
                "foooooo": "blah",
                "afoot": "bar",
            },
        ]
        expected = [
        ]
        self.assertEqual(expected, hunter.hunt(root))

        """
          Repeat scenario with negate=True
        """
        hunter.negate = True
        expected = [
            {
                "path": "/1",
                "tree": {
                    "foo": "car",
                },
            },
        ]

        self.assertEqual(expected, hunter.hunt(root))

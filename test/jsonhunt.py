"""
     Unit tests for jsonhunt command
"""

import re
import json

from unittest import TestCase
from bin.jsonhunt import Jsonhunt

class JsonhuntTest(TestCase):

    def test_SimpleKV(self):
        hunter = Jsonhunt(re.compile("foo"), re.compile("bar"), False)

        root = {
            "foo": "bar",
        }

        expected = [
            {
                "path": "/",
                "tree": {
                    "foo": "bar",
                },
            },
        ]

        self.assertEqual(expected, hunter.hunt(root))

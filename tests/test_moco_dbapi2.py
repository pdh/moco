#!/usr/bin/env python

import dbapi20
import unittest
import moco

from tests.base import MocoTestCase

class MocoTests(dbapi20.DatabaseAPI20Test):
    driver = moco
    connect_args = ()
    connect_kw_args = MocoTestCase.databases[0]

    lower_func = 'lower'

    def test_setoutputsize(self):
        pass

    def test_nextset(self):
        pass


def test_suite():
    return unittest.TestLoader().loadTestsFromName(__name__)


if __name__ == '__main__':
    unittest.main()

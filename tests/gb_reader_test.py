# -*- coding: utf-8 -*-
import unittest
import json
import io
from os.path import (
    join,
    abspath,
    dirname
)

import _setup
from libnano.fileio import gb_reader

LOCAL_DIR: str = abspath(dirname(__file__))


class TestGBReader(unittest.TestCase):

    def setUp(self):
        self.files = [ 'sample.gb',
                        'mds42_full.gb',
                        'mds42_recode.gb',
                        'sample_complex.gb',
                        'failed.gb'

        ]
    # end def

    def checkFile(self, fn, should_fail=False):
        fn_gb = join(LOCAL_DIR, 'test_data', fn)
        d_gb = gb_reader.parse(fn_gb)
        fn_json = fn_gb + '.json'
        with io.open(fn_json, 'r', encoding='utf-8') as fd_json:
            d_json = json.load(fd_json)
        if should_fail:
            self.assertNotEqual(d_gb['info'], d_json['info'])
        else:
            self.assertEqual(d_gb['info'], d_json['info'])
    # end def

    def test_checkFiles(self):
        for fn in self.files:
            self.checkFile(fn, should_fail=('fail' in fn))
# end class


if __name__ == '__main__':
    unittest.main(verbosity=2)
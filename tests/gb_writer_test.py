import unittest
import sys
import os
from os.path import (
    join,
    abspath,
    dirname
)
import json
from tempfile import NamedTemporaryFile
import filecmp

LOCAL_DIR = abspath(dirname(__file__))
# For package imports
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

import _setup
from libnano.fileio import gb_reader, gb_writer

IS_PY_3 = int(sys.version_info[0] > 2)

class TestGBWriter(unittest.TestCase):

    def setUp(self):
        self.good_files = [ 'sample.gb',
                        'mds42_full.gb',
                        'mds42_recode.gb',
                        'sample_complex.gb'
        ]
        self.bad_files = ['failed.gb', # fails due to ApE double COMMENT key
                            'mds42_recode_biopython.gb' # biopython has 80 character lines and we do 79
                        ]
        self.maxDiff = None     # assertEquals will print out whole diff
    # end def

    def checkFile(self, fn, should_be_true):
        fn_gb = join(LOCAL_DIR, 'test_data', fn)
        d_gb = gb_reader.parse(fn_gb, is_ordered=True)

        if IS_PY_3:
            f_temp = NamedTemporaryFile(mode='w', delete=False, encoding='utf-8')
        else:
            f_temp = NamedTemporaryFile(mode='w', delete=False)
        gb_writer.write(f_temp, d_gb)
        f_temp.close()
        if should_be_true:
            self.assertTrue(filecmp.cmp(fn_gb, f_temp.name))
        else:
            self.assertFalse(filecmp.cmp(fn_gb, f_temp.name))
        os.unlink(f_temp.name)
        self.assertFalse(os.path.exists(f_temp.name))
    # end def

    def test_goodFiles(self):
        for fn in self.good_files:
            self.checkFile(fn, True)

    def test_badFiles(self):
        for fn in self.bad_files:
            self.checkFile(fn, False)
# end class


if __name__ == '__main__':
    unittest.main(verbosity=2)
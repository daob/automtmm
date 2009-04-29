#!/usr/bin/python
import sys
import os
import unittest

base_path = '/home/daob/work/automtmm'
sys.path.append(base_path)
import parse_lisrel


class TestParseFunctions(unittest.TestCase):

    def setUp(self):
        test_file = open(os.path.join(base_path, 
                         'tests/ess-round2/r2jobPT.LS8'), 'rb')
        self.test_input = test_file.read()
        test_file.close()

    def test_get_ngroups(self):
        self.assertEqual(parse_lisrel.get_ngroups(self.test_input), 2)

    def test_get_dimensions(self):
        dim = parse_lisrel.get_dimensions(self.test_input)
        self.assertEqual(dim[0]['NX'], 0)
        self.assertEqual(dim[0]['NY'], 9)
        self.assertEqual(dim[0]['NK'], 6)
        self.assertEqual(dim[0]['NE'], 9)
        self.assertEqual(dim[1]['NX'], 0)
        self.assertEqual(dim[1]['NY'], 91)
        self.assertEqual(dim[1]['NK'], 6)
        self.assertEqual(dim[1]['NE'], 9)

    def test_get_matrix_forms(self):
        forms = parse_lisrel.get_matrix_forms(self.test_input)
        self.assertEqual(len(forms), 2)
        self.assertEqual(forms[0]['LY'], {'Form':'FU', 'Free':'FI'})
        self.assertEqual(forms[0]['TE'], {'Form':'SY', 'Free':'FI'})
        self.assertEqual(forms[0]['PS'], {'Form':'DI', 'Free':'FI'})
        self.assertEqual(forms[0]['BE'], {'Form':'FU', 'Free':'FI'})
        self.assertEqual(forms[0]['GA'], {'Form':'FU', 'Free':'FI'})
        self.assertEqual(forms[0]['PH'], {'Form':'SY', 'Free':'FI'})
        self.assertEqual(forms[1]['LY'], {'Form':'FU', 'Free':'FI'})
        self.assertEqual(forms[1]['TE'], {'Form':'SY', 'Free':'FI'})
        self.assertEqual(forms[1]['PS'], {'Form':'DI', 'Free':'IN'})
        self.assertEqual(forms[1]['BE'], {'Form':'FU', 'Free':'IN'})
        self.assertEqual(forms[1]['GA'], {'Form':'FU', 'Free':'IN'})
        self.assertEqual(forms[1]['PH'], {'Form':'SY', 'Free':'IN'})


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestParseFunctions)
    unittest.TextTestRunner(verbosity=2).run(suite)


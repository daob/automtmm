#!/usr/bin/python
import sys
import os
import unittest

base_path = '/home/daob/work/automtmm'
sys.path.append(base_path)
from parse_lisrel import LisrelInput


class TestInputGB(unittest.TestCase):

    def setUp(self):
        self.test_input = LisrelInput(os.path.join(base_path, 
                            'tests/ess-round3/GB/IMSMETN/r3imsmetnGB.LS8'))

    def test_get_ngroups(self):
        self.assertEqual(self.test_input.get_ngroups(), 3)

    def test_get_dimensions(self):
        dim = self.test_input.get_dimensions()
        self.assertEqual(dim[0]['NX'], 0)
        self.assertEqual(dim[0]['NY'], 12)
        self.assertEqual(dim[0]['NK'], 7)
        self.assertEqual(dim[0]['NE'], 12)
        self.assertEqual(dim[1]['NX'], 0)
        self.assertEqual(dim[1]['NY'], 12)
        self.assertEqual(dim[1]['NK'], 7)
        self.assertEqual(dim[1]['NE'], 12)

    def test_get_matrix_forms(self):
        forms = self.test_input.get_matrix_forms()
        self.assertEqual(len(forms), 3)
        self.assertEqual(forms[0]['LY'], {'Form':'FU', 'Free':'FI'})
        self.assertEqual(forms[0]['TE'], {'Form':'SY', 'Free':'FI'})
        self.assertEqual(forms[0]['PS'], {'Form':'SY', 'Free':'FI'})
        self.assertEqual(forms[0]['BE'], {'Form':'FU', 'Free':'FI'})
        self.assertEqual(forms[0]['GA'], {'Form':'FU', 'Free':'FI'})
        self.assertEqual(forms[0]['PH'], {'Form':'SY', 'Free':'FI'})
        self.assertEqual(forms[1]['LY'], {'Form':'FU', 'Free':'FI'})
        self.assertEqual(forms[1]['TE'], {'Form':'SY', 'Free':'FI'})
        self.assertEqual(forms[1]['PS'], {'Form':'SY', 'Free':'IN'})
        self.assertEqual(forms[1]['BE'], {'Form':'FU', 'Free':'IN'})
        self.assertEqual(forms[1]['GA'], {'Form':'FU', 'Free':'IN'})
        self.assertEqual(forms[1]['PH'], {'Form':'SY', 'Free':'IN'})
        self.assertEqual(forms[2]['LY'], {'Form':'FU', 'Free':'FI'})
        self.assertEqual(forms[2]['TE'], {'Form':'SY', 'Free':'FI'})
        self.assertEqual(forms[2]['PS'], {'Form':'SY', 'Free':'IN'})
        self.assertEqual(forms[2]['BE'], {'Form':'FU', 'Free':'IN'})
        self.assertEqual(forms[2]['GA'], {'Form':'FU', 'Free':'IN'})
        self.assertEqual(forms[2]['PH'], {'Form':'SY', 'Free':'IN'})


class TestInputPT(unittest.TestCase):

    def setUp(self):
        self.path = os.path.join(base_path, 
                            'tests/ess-round2/r2jobPT.LS8')
        self.test_input = LisrelInput(self.path)

    def test_get_ngroups(self):
        self.assertEqual(self.test_input.get_ngroups(), 2)

    def test_get_dimensions(self):
        dim = self.test_input.get_dimensions()
        self.assertEqual(dim[0]['NX'], 0)
        self.assertEqual(dim[0]['NY'], 9)
        self.assertEqual(dim[0]['NK'], 6)
        self.assertEqual(dim[0]['NE'], 9)
        self.assertEqual(dim[1]['NX'], 0)
        self.assertEqual(dim[1]['NY'], 91)
        self.assertEqual(dim[1]['NK'], 6)
        self.assertEqual(dim[1]['NE'], 9)

    def test_get_matrix_forms(self):
        forms = self.test_input.get_matrix_forms()
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

    def input_writes_output(self, input_obj):
        import re
        str = input_obj.get_modified_input()
        reg = re.compile(r'OU[^\n\r$]+PH[ ]*=[ ]*[A-Z]+\.[A-Z]', 
                input_obj.re_flags)
        return(len(reg.findall(str)) > 0)
    
    def test_get_modified_input(self):
        self.assert_(self.input_writes_output(self.test_input))

    def test_write_to_file(self):
        str = self.test_input.get_modified_input()
        self.test_input.write_to_file(str)
        orig_str = self.test_input.input_text
        f = open(self.path + '.backup')
        self.assertEqual(f.read(), orig_str)
        f.close()
        new_input = LisrelInput(self.path)
        self.assert_(self.input_writes_output(new_input))

if __name__ == '__main__':
    suite_PT = unittest.TestLoader().loadTestsFromTestCase(TestInputPT)
    suite_GB = unittest.TestLoader().loadTestsFromTestCase(TestInputGB)
    suite = unittest.TestSuite([suite_PT, suite_GB])
    unittest.TextTestRunner(verbosity=2).run(suite)


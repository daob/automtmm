#!/usr/bin/python
import sys
import os
import unittest
import numpy as np

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
        self.assertEqual(dim[1]['NY'], 9)
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

    def test_get_matrices(self):
        mats = self.test_input.get_matrices(path = 'temp')
        ly_1 = np.diag([1.,1.,-1.,1.,1.,-1.,0.,0.,0.])
        assert_mats_equal(mats['LY'][0], ly_1, self)
        ly_2 = np.diag([1.,1.,-1.,0.,0.,0.,1.,1.,-1.])
        assert_mats_equal(mats['LY'][1], ly_2, self)

        ga_1 = np.matrix([[ 
          0.20472,  0.     ,  0.     ,  1.     ,  0.     ,  0.     ],
        [ 0.     ,  0.18653,  0.     ,  1.     ,  0.     ,  0.     ],
        [ 0.     ,  0.     ,  0.19128,  1.     ,  0.     ,  0.     ],
        [ 3.2513 ,  0.     ,  0.     ,  0.     ,  1.     ,  0.     ],
        [ 0.     ,  3.0898 ,  0.     ,  0.     ,  1.     ,  0.     ],
        [ 0.     ,  0.     ,  3.3435 ,  0.     ,  1.     ,  0.     ],
        [ 3.2535 ,  0.     ,  0.     ,  0.     ,  0.     ,  1.     ],
        [ 0.     ,  3.2535 ,  0.     ,  0.     ,  0.     ,  1.     ],
        [ 0.     ,  0.     ,  3.2535 ,  0.     ,  0.     ,  1.     ]])
        assert_mats_equal(mats['GA'][0], ga_1, self)

        ga_2 = np.matrix([[ 0.20472,  0.     ,  0.     ,  1.     ,  0.     ,  0.     ],
        [ 0.     ,  0.18653,  0.     ,  1.     ,  0.     ,  0.     ],
        [ 0.     ,  0.     ,  0.19128,  1.     ,  0.     ,  0.     ],
        [ 3.2513 ,  0.     ,  0.     ,  0.     ,  1.     ,  0.     ],
        [ 0.     ,  3.0898 ,  0.     ,  0.     ,  1.     ,  0.     ],
        [ 0.     ,  0.     ,  3.3435 ,  0.     ,  1.     ,  0.     ],
        [ 3.2535 ,  0.     ,  0.     ,  0.     ,  0.     ,  1.     ],
        [ 0.     ,  3.2535 ,  0.     ,  0.     ,  0.     ,  1.     ],
        [ 0.     ,  0.     ,  3.2535 ,  0.     ,  0.     ,  1.     ]])
        assert_mats_equal(mats['GA'][1], ga_2, self)
        print mats
        
def assert_mats_equal(mat1, mat2, by_obj):
    """Convenience function to assert that two matrices or arrays have the same
       dimensions and all elements are approximately equal (within machine tolerance)."""
    by_obj.assertEqual(mat1.shape, mat2.shape)
    for i in range(mat1.shape[0]):
        for j in range(mat1.shape[1]):
            by_obj.assertAlmostEqual(mat2[i, j], mat1[i, j])

if __name__ == '__main__':
    suite_PT = unittest.TestLoader().loadTestsFromTestCase(TestInputPT)
    suite_GB = unittest.TestLoader().loadTestsFromTestCase(TestInputGB)
    suite = unittest.TestSuite([suite_PT, suite_GB])
    unittest.TextTestRunner(verbosity=8).run(suite)


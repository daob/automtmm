import unittest
from LisrelMatrix import SymmetricMatrix, DiagonalMatrix

phi_test_txt = """

         PHI         

               KSI 1      KSI 2      KSI 3      KSI 4      KSI 5      KSI 6
            --------   --------   --------   --------   --------   --------
    KSI 1          0
    KSI 2        109          0
    KSI 3        110        111          0
    KSI 4          0          0          0         13
    KSI 5          0          0          0          0         14
    KSI 6          0          0          0          0          0         15

        """

te_test_txt = """

         THETA-EPS   

               VAR 1      VAR 2      VAR 3      VAR 4      VAR 5      VAR 6
            --------   --------   --------   --------   --------   --------
                 112        113        114          0          0          0

         THETA-EPS   

               VAR 7      VAR 8      VAR 9
            --------   --------   --------
                 118        119        120



"""


class ParameterizedMatrixTestCase(unittest.TestCase):
    def setUp(self):
        self.mat = SymmetricMatrix('TeSt')
                 
    def test_short_name(self):
        # Make sure the short name is correctly set
        self.assertEqual(self.mat.short_name, 'TE')

    def test_re_lismat_phi(self):
        # Test regular expression that reads matrices on PHI param matrix
        self.assertEqual(self.mat.re_lismat.findall(phi_test_txt),
            ['    KSI 1          0\n    KSI 2        109          0\n    KSI 3        110        111          0\n    KSI 4          0          0          0         13\n    KSI 5          0          0          0          0         14\n    KSI 6          0          0          0          0          0         15',])
        
    def test_re_lismat_te(self):
        # Test regular expression that reads matrices on TE param matrix
        self.assertEqual(self.mat.re_lismat.findall(te_test_txt),
                ['                 112        113        114          0          0          0',
 '                 118        119        120'])

    def test_parse_parameters(self):
        # Test that parse_parameters correctly extracts the parameter numbers

        self.assertEqual(self.mat.parse_parameters(phi_test_txt),
                [ 0, 109, 0, 110, 111, 0, 0, 
                  0, 0, 13, 0, 0, 0, 0, 14, 0, 0, 0, 0, 0, 15])

        self.assertEqual(self.mat.parse_parameters(te_test_txt),
                [112,113,114,0,0,0,118,119,120]) 


class SymmetricMatrixTestCase(unittest.TestCase):
    
    def setUp(self):
        self.mat = SymmetricMatrix('PHI')

    def test_infer_size(self):
        self.mat.param_num_vector = self.mat.parse_parameters(phi_test_txt)
        self.mat.infer_size() # IO
        self.assertEqual(self.mat.ncols, 6)
        self.assertEqual(self.mat.nrows, 6)
        self.assertEqual(self.mat.order, 6)
        self.assertEqual(self.mat.shape, (6, 6))

    def test_read_parameter_numbers(self):
        # Test whether the following snippet from a LISREL output is correctly
        # read in as a 6x6 parameter number matrix
        should_be = [[0,109,110,0,0,0], [109, 0, 111, 0, 0, 0], 
                [110, 111, 0, 0, 0, 0], [0,0,0,13,0,0], 
                [0,0,0,0,14,0], [0,0,0,0,0,15]]        

        self.mat.read_parameter_numbers(phi_test_txt)
        self.assertEqual(self.mat.param_nums, should_be)



class DiagonalMatrixTestCase(unittest.TestCase):
    
    def setUp(self):
        self.mat = DiagonalMatrix('THETA-EPS')

    def test_infer_size(self):
        self.mat.param_num_vector = self.mat.parse_parameters(te_test_txt)
        self.mat.infer_size() # IO
        self.assertEqual(self.mat.ncols, 9)
        self.assertEqual(self.mat.nrows, 9)
        self.assertEqual(self.mat.shape, (9, 9))

    def test_read_parameter_numbers(self):
        # Test whether the following snippet from a LISREL output is correctly
        # read in as a 6x6 parameter number matrix
        should_be = \
            [[112, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 113, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 114, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 118, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 119, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 120]]

        self.mat.read_parameter_numbers(te_test_txt)
        self.assertEqual(self.mat.param_nums, should_be)

if __name__ == '__main__':
    unittest.main()

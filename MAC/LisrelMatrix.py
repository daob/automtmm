"""LISREL Matrix classes: Symmetric, Diagonal and Full"""

import re
from copy import deepcopy

from Helpers import Helper


class ParameterizedMatrix(object):
    """Base class for LisrelMatrices."""

    re_lines = re.compile(r'[ ]+--------')
    re_ws = re.compile(r'^[\n\r]$')
    re_lismat = re.compile(r"""(?:[ ]+--------)+? # One+ groups of LISREL's separator lines
                         [\n\r]     # Everything after the separators is the parameters
                         (.+?)       # Parameter values in whatever format
                         [\n\r]{2}  # blank line signals end of section.""",
            re.DOTALL|re.VERBOSE)
    re_cleannums = re.compile(r'([\n\r]|[ ]+([A-Za-z_]+)( \d+){0,1})')

    nrows = None 
    ncols = None
    param_nums = None # Actual matrix with parameter numbers
    param_num_vector = None # Parameter numbers in raw vector form

    def __init__(self, name):
        self.name = name
        self.short_name = name[:2].upper()

    def parse_parameter_numbers(self, txt):
        """[IO]  Specifc method to infer nrows and ncols & create 
        appropriate-size values and numbers matrices."""

        self.param_num_vector = self.parse_parameters(txt)
        self.infer_size() # IO; requires self.param_num_vector to be set

        return self.matrix_from_vector(self.param_num_vector)

    def parse_parameters(self, txt, num_type=int):
        """[Pure]
        Take the text of the matrix as output from LISREL and return a list of
        the numbers found in the matrix. 
        num_type decides whether to convert the numbers to int (parameter
        numbers) or float (values)"""
        # Take advantage of LISREL's printing the separators ------ above the
        # first line containing the numbers of interest. Uses regular
        # expression to find the numbers needed, taking into account that
        # LISREL sometimes splits matrices across several parts when they
        # exceed the screen width.
        mlist = self.re_lismat.findall(txt)    # List of results (for splits)

        # If you want to understand how this works, read from bottom to top:
        return [num_type(number) for number in    # Convert to wanted value
            re.split(r'[ ]+',           # Split result on whitespace
            self.re_cleannums.sub('',   # Remove any variable labels from text
                ' '.join(mlist))       # Join matrices split by LISREL
        ) if number != '']              # Remove any remaining empty entries

    def read_parameter_numbers(self, txt):
        """[IO]
        Read parameter numbers into list of lists and set self.values to that
        list."""
        self.param_nums = self.parse_parameter_numbers(txt)

    @property
    def shape(self):
        "Rows and columns in a tuple, just as numpy does"
        return (self.nrows, self.ncols)

    def read_parameter_values(self, txt):
        """[IO] Read parameter numbers (abstract)"""
        raise NotImplementedError()

    def infer_size(self):
        "Infer the size of the matrix (abstract method)"
        raise NotImplementedError()

    def matrix_from_vector(self, params):
        "Create a matrix from a vector (abstract method)"
        raise NotImplementedError()
        

class SymmetricMatrix(ParameterizedMatrix):
    """A matrix which has been treated as SY within LISREL"""

    def matrix_from_vector(self, params):
        """[Pure]  take a vector of parameters, and, given the size of the
        symmetric, matrix, return a symmetric matrix with the appropriate
        values set. Can be used for both parameter numbers and values."""

        poplist = deepcopy(params)
        # Pop the first few items off the list, adding on zeroes, increasing
        # the number of items to pop per row (1,2,3,..order)
        resmat = \
            [   [poplist.pop(0) for n in xrange(self.order - i)] + [0,]*i
            for i in reversed(xrange(self.order))]

        # Copy the lower-diagonal elements to the upper diagonal to make a
        # symmetric matrix (operates on the resmat directly):
        Helper.symmetrize_list_matrix(resmat, self.shape) # IO

        return resmat

    def infer_size(self):
        """[IO]  Symmetric-specifc method to infer nrows and ncols"""
        self.nrows = Helper.nrows_symm(len(self.param_num_vector))
        self.ncols = self.nrows # Symmetric

    @property
    def order(self):
        "Just nice to use the same words as in algebra"
        return self.ncols
    

class DiagonalMatrix(ParameterizedMatrix):
    """A matrix which has been treated as DIAGONAL within LISREL"""


    @staticmethod
    def matrix_from_vector(params):
        """[Pure]  take a vector of parameters, and
        return a diagonal matrix with the appropriate 
        values set. Can be used for both parameter numbers and values."""

        order = len(params)
        resmat = [[0,]*order for i in range(order)]
        for i in range(order):
            resmat[i][i] = params[i]

        return resmat

    def infer_size(self):
        """[IO]  Symmetric-specifc method to infer nrows and ncols"""
        self.nrows = len(self.param_num_vector)
        self.ncols = self.nrows # Symmetric

    @property
    def order(self):
        "Just nice to use the same words as in algebra"
        return self.ncols
    

class FullMatrix(ParameterizedMatrix):
    """A matrix which has been treated as DIAGONAL within LISREL"""

    # A regex used to count the number of rows. Won't work when split across
    # multiple rows (will count double)
    re_row = re.compile(r'[ ]+([a-zA-Z_]+)(?: \d+){0,1} (?:(?:[ ]+\d)+)[\n\r]')

    def __init__(self, name, param_num_txt):
        """FullMatrix requires that the actual text is saved in the object so
        the shape of the matrix can be inferred."""
        self.param_num_txt = param_num_txt
        super(FullMatrix, self).__init__(name)

    def matrix_from_vector(self, params):
        """[Pure]  take a vector of parameters, and
        return a full matrix with the appropriate 
        values set. Can be used for both parameter numbers and values."""
        resmat = [self.param_num_vector[i*self.ncols : (i + 1)*self.ncols] \
                for i in range(self.nrows)]
        return resmat

    def infer_size(self):
        """[IO] Full-specifc method to infer nrows and ncols"""

        # Just count the number of rows in the parameter specification part
        results = self.re_row.findall(self.param_num_txt)

        self.nrows = len(results)
        self.ncols = len(self.param_num_vector) / self.nrows

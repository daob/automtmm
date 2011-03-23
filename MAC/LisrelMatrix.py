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


    def __init__(self, name):
        self.name = name
        self.short_name = name[:2].upper()

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

    def read_parameter_values(self, txt):
        """[IO]
        Read parameter numbers"""
        pass

    @property
    def shape(self):
        return (self.nrows, self.ncols)

    def parse_parameter_numbers(self, txt):
        pass

    def infer_size(self):
        pass

class SymmetricMatrix(ParameterizedMatrix):
    """A matrix which has been treated as SY within LISREL"""

    def parse_parameter_numbers(self, txt):
        """[IO]  Symmetric-specifc method to infer nrows and ncols & create 
        appropriate-size values and numbers matrices."""

        self.param_num_vector = self.parse_parameters(txt)
        self.infer_size() # IO; requires self.param_num_vector to be set

        return self.symmetric_from_vector(self.param_num_vector)

    def symmetric_from_vector(self, params):
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

    def parse_parameter_numbers(self, txt):
        """[IO]  Diagonal-specifc method to infer nrows and ncols & create 
        appropriate-size values and numbers matrices."""

        self.param_num_vector = self.parse_parameters(txt)
        self.infer_size() # IO; requires self.param_num_vector to be set

        return self.diagonal_from_vector(self.param_num_vector)

    @staticmethod
    def diagonal_from_vector(params):
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
    

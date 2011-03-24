"""Group class performs group-level operations"""

from LisrelMatrix import matrix_names 
from LisrelMatrix import FullMatrix, DiagonalMatrix, SymmetricMatrix


class Group(object):
    """Group information and group-level operations"""

    matrices = [] # list of matrices in this group

    def __init__(self, name, number):
        self.name = name.strip()
        self.number = int(number)

    

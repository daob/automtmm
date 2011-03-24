"""Group class performs group-level operations"""

import re

from LisrelMatrix import matrix_names 
from LisrelMatrix import FullMatrix, DiagonalMatrix, SymmetricMatrix


class Group(object):
    """Group information and group-level operations"""

    matrices = None # list of matrices in this group

    re_splitmat = re.compile(r"(%s)" % '|'.join(matrix_names.keys()))
    re_strip = re.compile(r'(^[\s]+(?=\w*)|\s+$)') 

    def __init__(self, name, number):
        self.name = name.strip()
        self.number = int(number)

    def __repr__(self):
        return "Group %d: '%s'" % (self.number, self.name)

    def __unicode__(self):
        return repr(self)

    def create_matrices(self, txt):
        """Detect standardized matrices and add them to matrices list"""
        mat_txts = self.split_matrices(txt)
        self.matrices = []

        for mat_txt in mat_txts:
            matrix = FullMatrix(mat_txt['name'])
            matrix.read_standardized(mat_txt['txt_std'])
            self.matrices.append(matrix)
    
    def split_matrices(self, txt):
        """Given a snippet for this group with different matrices, split into
        different snippets suitable for matrix.read_standardized and return
        that"""
        retl = self.re_splitmat.split(txt)
        names = self.re_splitmat.findall(txt)
        
        retl = [r for r in                  
                [self.re_splitmat.sub('', # Remove matrixnames from text
                    self.re_strip.sub('', rel)) # strip whitespace
                for rel in retl] if r != '']    # rm matnames & whitespace-only
               
        reslist = [] # Will contain joined texts

        # Figure out if a list element is a continuation of a previous matrix
        # or a new one. 
        prev_name = None
        for i, name in enumerate(names):
            if name == prev_name:  # If continuation, 
                reslist[-1]['txt_std'] += '\r\n\r\n' + retl[i]  # Just concatenate text with previous
            else:  # New matrix
                # Add to list of matrix texts
                reslist.append({'txt_std':retl[i], 'name':name})
            prev_name = name

        return reslist

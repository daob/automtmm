"""Classes to deal with LISREL input and output files."""
#!/usr/bin/python
import os
import re
from copy import deepcopy
import numpy as np


class LisrelInput:
    """Functions to get information about number of groups and matrix form
       from a LISREL self.input_text file."""

    def __init__(self, path = '', text = ''):
        "Set self.input_text or fail."
        if text == '': # read from file
            input_file = open(path, 'rb')
            self.input_text = input_file.read()
            input_file.close()
            self.path = path # remember path for write
        else:
            self.input_text = text
        self.re_flags = re.MULTILINE | re.IGNORECASE 
        self.mats = { 
             'LY': {'Form':'FU', 'Free':'FI'},
             'LX': {'Form':'FU', 'Free':'FI'}, 
             'TE': {'Form':'DI', 'Free':'FR'}, 
             'TD': {'Form':'DI', 'Free':'FR'}, 
             'BE': {'Form':'ZE', 'Free':'FI'}, 
             'GA': {'Form':'FU', 'Free':'FR'}, 
             'PH': {'Form':'SY', 'Free':'FR'}, 
             'PS': {'Form':'DI', 'Free':'FR'}, 
             'TY': {'Form':'VE', 'Free':'FI'},
             'TX': {'Form':'VE', 'Free':'FI'}, 
             'KA': {'Form':'VE', 'Free':'FI'}, 
             'AL': {'Form':'VE', 'Free':'FI'} }


    def get_matrix_forms(self):
        """Retrieve 'form' (full, symmetrix, zero, diagonal, ... 
           and free or fixed) Of matrices for LISREL model for each group.
           Returns an <ngroups> list of dictionaries."""
            
        mats = self.mats
        ngroups = self.get_ngroups()
        forms = []
        start_re = r'^[ \t]*MO[A-Z0-9=, \t]+'
    
        for igroup in range(ngroups):
            forms.append(deepcopy(mats))
        
            for key in mats.keys():
                find_n = start_re + key + r'[ ]*=[ ]*([A-Z,]+)'
                find = re.findall(find_n, self.input_text, self.re_flags)
                if len(find) > 0:
                    tmp = find[igroup].split(',')
                    if len(tmp) > 1:
                        forms[igroup][key]['Form'] = tmp[0].upper()
                        forms[igroup][key]['Free'] = tmp[1].upper()
                    elif tmp[0].upper() == 'IN':
                        forms[igroup][key]['Form'] = forms[igroup - 1][key]\
                                ['Form']
                        forms[igroup][key]['Free'] = 'IN'
        return(forms)
    
    def get_ngroups(self):
        "Retrieve number of groups. Fails if file contains stacked analyses."
        model_line = r'^[ \t]*MO[^N]+'
        res = re.findall(model_line, self.input_text, self.re_flags)
        return(len(res))
    
    def get_dimensions(self):
        """Retrieve number of x, y, eta, and ksi variables for each group.
           Returns a <ngroups> list of dictionaries."""
    
        ngroups = self.get_ngroups()
        dims = []
        nvar = {'NX':0, 'NY':0, 'NE':0, 'NK':0}
        start_re = r'^[ \t]*MO[A-Z0-9=, \t]+'
        for igroup in range(ngroups):
            dims.append(deepcopy(nvar))
        
            for key in nvar.keys():
                find_n = start_re + key + r'[ ]*=[ ]*([0-9]+)'
                find = re.findall(find_n, self.input_text, self.re_flags)
                if len(find) > 0:
                    dims[igroup][key] = int(find[igroup])
        return(dims)

    def get_modified_input(self, extras = ' MI AD=OFF IT=200 NS'):
        """Modifies input to write matrix results to files. Returns string."""
        outstr = ' '.join(["%s=%s.out"%(key, key) for key in self.mats.keys()])
        outstr += ' PV=PV.out SV=SV.out' + extras
        reg_out = re.compile(r'^[ ]*(OU[A-Z0-9=. \'"]+)', self.re_flags)
        return(reg_out.sub(r'OU ' + outstr, self.input_text))

    def write_to_file(self, new_text, path = ''):
        """Write the input text to a file. Overwrites the original 
           (making a backup) if no argument is given."""
        if path == '':
            path = self.path
            b_file = open(path + '.backup', 'w')
            b_file.write(self.input_text)
            b_file.close()

        w_file = open(path, 'w')
        w_file.write(new_text)
        w_file.close()

    def get_matrix_shape(self, matname, groupnum):
        """Returns the shape of a given LISREL matrix <matname> 
            in group <groupnum>."""
        dim = self.get_dimensions()
        dim = dim[groupnum]

        matorderdict = \
        {'LY': (dim['NY'], dim['NE']),
         'LX': (dim['NX'], dim['NE']),
         'TE': (dim['NY'], dim['NY']),
         'TD': (dim['NX'], dim['NX']),
         'BE': (dim['NE'], dim['NE']),
         'GA': (dim['NK'], dim['NE']),
         'PH': (dim['NK'], dim['NK']),
         'PS': (dim['NE'], dim['NE']),
         'TY': (dim['NY'], 0),
         'TX': (dim['NX'], 0),
         'KA': (dim['NE'], 0),
         'AL': (dim['NK'], 0),
        }
        return(matorderdict[matname])

    def lisrel_science_to_other(self, string):
        '''Finds numbers of the form 0.12D-04 and converts them to a list of
           Python floats.
           
           LISREL Scientific notation is different from the regular one. 
           Normally an e or E is used to mean 'multiplied by 10 to the power
           of...'. LISREL uses a D, confusing Python and R.'''
        numbers = re.compile(r'([0-9.DE\-\\+]+)', self.re_flags)
        numbers = [float(num.replace('D','e')) for 
                        num in numbers.findall(string) ]
        return(numbers)

    def get_matrices(self, path = ''):
        """Read matrices from output files <MAT>.out, taking into account 
           the form of the matrix. Returns dict of <ngroups> list of 
           NumPy.matrices read from the files."""
        if path == '':
            path = self.path
        mats = deepcopy(self.mats)
        matforms = self.get_matrix_forms()[0]
        ngroups = self.get_ngroups()

        for matname in self.mats.keys():
            matf = file(os.path.join(path, matname+'.out'), 'rb')
            mat_s = matf.read()
            numbers = self.lisrel_science_to_other(mat_s)
            mat = []
            if matforms[matname]['Form'] == 'DI': # or vec
                for igrp in range(ngroups):
                    order = self.get_matrix_shape(matname, igrp)[0]
                    mat.append(np.diag(numbers[ igrp*order : 
                                (igrp*order) + order ]))

            elif matforms[matname]['Form'] == 'FU': 
                                    
                for igrp in range(ngroups):
                    order = self.get_matrix_shape(matname, igrp)
                    matlen = order[0] * order[1]
                    arr_group = np.array(numbers[ igrp*matlen : 
                            (igrp*matlen) + matlen ])
                    # LISREL changes matrices specified as FULL to 
                    # DIAGONAL automatically if possible:
                    if len(numbers)/ngroups != matlen and \
                            len(numbers)/ngroups == order[0]:
                        gmat = np.diag(numbers[igrp*order[0] : 
                                (igrp*order[0]) + order[0]])
                    else:                       
                        gmat = np.matrix(np.reshape(arr_group, 
                                    (order[1], order[0])))
                    mat.append(gmat)
            
            elif matforms[matname]['Form'] == 'SY': 
                for igrp in range(ngroups):
                    nrows, ncols = self.get_matrix_shape(matname, igrp)
                    offset = igrp * nrows*(nrows + 1)/2
                    print "ncols for %s: %d" % (matname,ncols)
                    print numbers
                    symat = []
                    start_prev = 0
                    for row in range(nrows):
                        start = row + start_prev
                        start += offset
                        tmp = numbers[ start:start+row+1 ]
                        tmp.extend([0] * (ncols - row - 1))
                        symat.append(tmp)
                        start_prev = start
#symat = symmetrize_matrix(np.matrix(symat))
                    mat.append(symat)
            else: 
                mat = '?'
                
            mats[matname] = mat
            matf.close()
        return(mats)

    def lisrel_symmat_to_mm(self, path):
        """argument: path to symmetric matrix output"""
        pass

def symmetrize_matrix(mat):
    """mat is a NumPy.matrix or .array. Copies the lower diagonal elements
       to the upper diagonal elements."""
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            mat[i, j] = mat[j, i]
    return mat

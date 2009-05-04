"""Classes to deal with LISREL input and output files."""
#!/usr/bin/python
import os, sys, re, subprocess
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

    def get_modified_input(self, extras = ' MI AD=OFF IT=200 NS SC'):
        """Modifies input to write matrix results to files, and converts relative
           paths in LISREL input to absolute paths. Returns string."""
        outstr = ' '.join(["%s=%s.out"%(key, key) for key in self.mats.keys()])
        outstr += ' PV=PV.out SV=SV.out' + extras
        reg_out = re.compile(r'^[ ]*(OU[A-Z0-9=. \'"]+)', self.re_flags)
        reg_inp = re.compile(r'file[ ]*=[ ]*([^ \r/\n\t$]+)[ \t\r\n$]', self.re_flags)
        modded = reg_out.sub(r'OU ' + outstr, self.input_text)
        modded = reg_inp.sub(r"file = %s%s\1" % 
                                ( os.path.abspath(os.path.dirname(self.path)),
                                  os.sep), 
                             modded)
        return(modded)

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
         'TY': (dim['NY'], 1),
         'TX': (dim['NX'], 1),
         'KA': (dim['NE'], 1),
         'AL': (dim['NK'], 1),
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
            if len(numbers) == 0: # fill it with zeroes
                shape = self.get_matrix_shape(matname, 0)
                numbers = [0.0] * (shape[0] * shape[1] * ngroups)
            mat = []
            if matforms[matname]['Form'] == 'DI': # or vec
                for igrp in range(ngroups):
                    order = self.get_matrix_shape(matname, igrp)[0]
                    mat.append(np.matrix(np.diag(numbers[ igrp*order : 
                                (igrp*order) + order ])))

            elif matforms[matname]['Form'] == 'FU': 
                                    
                for igrp in range(ngroups):
                    order = self.get_matrix_shape(matname, igrp)
                    matlen = order[0] * order[1]
                    arr_group = np.matrix(numbers[ igrp*matlen : 
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
                    mat.append(np.matrix(gmat))
            
            elif matforms[matname]['Form'] == 'SY': 
                for igrp in range(ngroups):
                    nrows, ncols = self.get_matrix_shape(matname, igrp)
                    if len(numbers)/ngroups != matlen and len(numbers)/ngroups == nrows:
                        symat = np.diag(numbers[igrp*nrows : (igrp*nrows) + nrows])
                    else:    
                        offset = igrp * nrows*(nrows + 1)/2
                        symat = []
                        start_prev = offset
                        for row in range(nrows):
                            start = row + start_prev
                            tmp = numbers[ start:start+row+1 ]
                            tmp.extend([0.0] * (ncols - row - 1))
                            symat.append(tmp)
                            start_prev = start
                        symat = symmetrize_matrix(np.matrix(symat))
                    mat.append(symat)

            elif matforms[matname]['Form'] == 'VE': # vectors
                shape = self.get_matrix_shape(matname, igrp)
                veclen = sum(shape) - 1

                for igrp in range(ngroups):
                    vec = np.matrix(numbers[igrp*veclen : (igrp+1) * veclen])
                    vec.shape = shape
                    mat.append(vec)
                
            elif matforms[matname]['Form'] == 'ZE': # zero matrix
                nrows, ncols = self.get_matrix_shape(matname, igrp)
                zemat = np.matrix([0.0] * (nrows * ncols))
                zemat.shape = (nrows, ncols)
                for igrp in range(ngroups):
                    mat.append(zemat)
                
            else: # Unknown type
                for igrp in range(ngroups):
                    mat.append('Unknown LISREL matrix type')
                    
            mats[matname] = mat
            matf.close()

        return(mats)
    
    def standardize_matrices(self):
        """Returns the same kind of list as get_matrices, but
           standardizes some of them. See Bollen 1989:350-1. """
        mats = self.get_matrices(path = 'temp')
        smats = []
        for igrp in range(self.get_ngroups()):
            be = mats['BE'][igrp]
            ly = mats['LY'][igrp]
            te = mats['TE'][igrp]
            ga = mats['GA'][igrp]
            ph = mats['PH'][igrp]
            ps = mats['PS'][igrp]

            bi = (np.diag([1.]*be.shape[0]) - be).I
            Eee = bi * (ga*ph*ga.T + ps) * bi.T
            Eyy = ly * Eee * ly.T + te
            C = np.matrix(np.sqrt(np.diag(np.diag(Eee))))
        
            ga_s = C.I * ga * np.sqrt(np.diag(np.diag(ph)))
            ly_s = np.sqrt(np.diag(1/np.diag(Eyy))) * ly * C

            smats.append({'GA': ga_s, 'LY': ly_s})

        return(smats) 

    def run_lisrel(self, temp_path = ''):
        """Run LISREL executable on the input file. The output is written to temp_path.
           Raises an exception if the exit code of the LISREL executable is not 0."""
        if temp_path == '': # default temp dir is same as self.path
            temp_path = os.path.abspath(os.path.dirname(self.path)) 
        if os.name == 'posix': # Linux/BSD/Mac OS X/Cygwin
            exstr = 'wine Lisrel85.exe'
        elif os.name == 'nt': # Windows
            exstr = os.path.join(os.getenv('ProgramFiles', 'C:\\Program Files'), 
                    'Lisrel85.exe')
        cmd =[exstr, os.path.abspath(self.path),  'OUT']  
        curdir = os.getcwd()
        os.chdir(temp_path)
        retval = os.system(" ".join(cmd))
        os.chdir(curdir)

        if not retval == 0:
            raise Exception("LISREL stopped with an error.")

def symmetrize_matrix(mat):
    """mat is a NumPy.matrix or .array. Copies the lower diagonal elements
       to the upper diagonal elements."""
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            mat[i, j] = mat[j, i]
    return mat

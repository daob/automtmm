"""Classes to deal with LISREL input and output files."""
#!/usr/bin/python
import os, sys, re
from copy import deepcopy
import numpy as np

sys.path.append('/home/daob/work/automtmm/retrieve_results')
import read_maxima


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
        self.long_names = {'GAMMA':'GA', 'LAMBDA-Y':'LY',
            'THETA-EPS':'TE','THETA-DELTA':'TE','PHI':'PH',
            'PSI':'PS','BETA':'BE','PHI':'PH'
        }

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

    def get_modified_input(self):
        """Modifies input to write matrix results to files, and converts 
           relative paths in LISREL input to absolute paths. Returns string."""
        outstr = ' PV=PV.out EC=EC.out ' 
        outstr += ' '.join(["%s=%s.out"%(key, key) for key in self.mats.keys()])
        reg_out = re.compile(r'^[ ]*(OU[A-Z0-9=. \'"]+)(?![!]ins)', 
                self.re_flags)
        reg_inp = re.compile(r'file[ ]*=[ ]*([^ \r/\n\t$]+)[ \t\r\n$]', 
                self.re_flags)
        modded = reg_out.sub(r'\1 ' + outstr, self.input_text)
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
            sys.stderr.write('Reading matrix %s...' % matname)
            matf = file(os.path.join(path, matname+'.out'), 'rb')
            mat_s = matf.read()
            numbers = self.lisrel_science_to_other(mat_s)
            if len(numbers) == 0: # fill it with zeroes
                shape = self.get_matrix_shape(matname, 0)
                numbers = [0.0] * (shape[0] * shape[1] * ngroups)
            mat = []
            if matforms[matname]['Form'] == 'DI': # or vec
                sys.stderr.write('%s is a DIagonal matrix.\n' % matname)
                for igrp in range(ngroups):
                    order = self.get_matrix_shape(matname, igrp)[0]
                    mat.append(np.matrix(np.diag(numbers[ igrp*order : 
                                (igrp*order) + order ])))

            elif matforms[matname]['Form'] == 'FU': 
                sys.stderr.write('%s is a FUll matrix.\n' % matname)
                                    
                for igrp in range(ngroups):
                    order = self.get_matrix_shape(matname, igrp)
                    matlen = order[0] * order[1]
                    arr_group = np.matrix(numbers[ igrp*matlen : 
                            (igrp*matlen) + matlen ])
                    # LISREL changes matrices specified as FULL to 
                    # DIAGONAL automatically if possible:
                    if len(numbers)/ngroups != matlen and \
                            len(numbers)/ngroups == order[0]:
                        matforms[matname]['Form'] = 'DI' # change it to DI
                        gmat = np.diag(numbers[igrp*order[0] : 
                                (igrp*order[0]) + order[0]])
                    else:                       
                        gmat = np.matrix(np.reshape(arr_group, 
                                    (order[1], order[0])))
                    mat.append(np.matrix(gmat))
            
            elif matforms[matname]['Form'] == 'SY': 
                sys.stderr.write('%s is a SYmmetric matrix.\n' % matname)
                for igrp in range(ngroups):
                    nrows, ncols = self.get_matrix_shape(matname, igrp)
                    if len(numbers)/ngroups != matlen and \
                                               len(numbers)/ngroups == nrows:
                        matforms[matname]['Form'] = 'DI' # change it to DI
                        symat = np.diag(numbers[igrp*nrows:(igrp*nrows)+nrows])
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
                sys.stderr.write('%s is a VEctor.\n' % matname)
                shape = self.get_matrix_shape(matname, igrp)
                veclen = sum(shape) - 1

                for igrp in range(ngroups):
                    vec = np.matrix(numbers[igrp*veclen : (igrp+1) * veclen])
                    vec.shape = shape
                    mat.append(vec)
                
            elif matforms[matname]['Form'] == 'ZE': # zero matrix
                sys.stderr.write('%s is a ZEroed matrix.\n' % matname)
                nrows, ncols = self.get_matrix_shape(matname, igrp)
                zemat = np.matrix([0.0] * (nrows * ncols))
                zemat.shape = (nrows, ncols)
                for igrp in range(ngroups):
                    mat.append(zemat)
                
            else: # Unknown type
                sys.stderr.write('%s has an unknown type!\n' % matname)
                for igrp in range(ngroups):
                    mat.append('Unknown LISREL matrix type')
                    
            mats[matname] = mat
            matf.close()
            # cache forms including adjustments made automatically by LISREL
            self.matforms = matforms 
        return(mats)
    
    def standardize_matrices(self, path = 'temp'):
        """Returns the same kind of list as get_matrices, but
           standardizes some of them. See Bollen 1989:350-1. """
        sys.stderr.write('Calculating standardized matrices for %s...\n'%
                os.path.basename(self.path))
        mats = self.get_matrices(path = path)
        smats = []
        for igrp in range(self.get_ngroups()):
            sys.stderr.write('Getting matrices for group %d (igrp=%d)\n'%
                    (igrp+1,igrp))
            be = mats['BE'][igrp]
            ly = mats['LY'][igrp]
            te = mats['TE'][igrp]
            ga = mats['GA'][igrp]
            ph = mats['PH'][igrp]
            nullify_diagonal(ph)
            ps = mats['PS'][igrp]

            bi = (np.diag([1.]*be.shape[0]) - be).I
            Eee = bi * (ga*ph*ga.T + ps) * bi.T
            Eyy = ly * Eee * ly.T + te
            C = np.matrix(np.sqrt(np.diag(np.diag(Eee))))
        
            try:
                ga_s = C.I * ga * np.sqrt(np.diag(np.diag(ph)))
            except np.linalg.LinAlgError, e:
                sys.stderr.write(str(C) + "\n")
                sys.stderr.write("Error calculating inverse: %s\n" % str(e))
                ga_s = np.matrix([])

            ly_s = np.sqrt(np.diag(1/np.diag(Eyy))) * ly * C

            smats.append({'GA': ga_s, 'LY': ly_s})

        return(smats) 

    def run_lisrel(self, temp_path = ''):
        """Run LISREL executable on the input file. The output is written to 
           temp_path. Raises an exception if the exit code of the LISREL
           executable is not 0."""
        if temp_path == '': # default temp dir is same as self.path
            temp_path = os.path.abspath(os.path.dirname(self.path)) 
        if os.name == 'posix': # Linux/BSD/Mac OS X/Cygwin
            exstr = 'wine Lisrel85.exe'
        elif os.name == 'nt': # Windows
            exstr = os.path.join(os.getenv('ProgramFiles', 'C:\\Program Files'),
                        'Lisrel85.exe')
        sys.stderr.write('Running LISREL for %s,'%os.path.basename(self.path))
        cmd = [exstr, os.path.abspath(self.path),  'OUT']  
        sys.stderr.write('Command is "%s".\n' % ' '.join(cmd))
        curdir = os.getcwd()
        os.chdir(temp_path)
        retval = os.system(" ".join(cmd))
        os.chdir(curdir)

        if not retval == 0:
            raise Exception("LISREL stopped with an error.")
        else:
            sys.stderr.write('LISREL terminated normally.\n')


    def get_free_params(self, outpath=''):
        """Retrieve the free parameters of the model from the output path."""
        if not outpath: # assume the output is in same folder with same name
            outpath = os.path.splitext(self.path)[0] + '.OUT'
        if not os.path.exists(outpath):
            raise Exception('Please specify a LISREL output file.')
        
        in_specs = False # are we in the parameter specification part?
        in_mat = False # Are we reading a matrix
        which_mat = '' # name of the matrix
        try:
            matforms = self.matforms
        except AttributeError:
            matforms = self.get_matrix_forms()[0]
        igroup = 0 # group counter
        iline = 1 # line counter

        parspec = re.compile(r'^[ ]*Parameter Specifications[ \n\r]*$')
        end = re.compile(r'LISREL Estimates \(Maximum Likelihood\)[ \n\r]*$')
        matrix = re.compile(r"""^[ ]*(?P<matname>GAMMA|PHI|BETA|LAMBDA-Y|PSI|
                                       LAMBDA-X|THETA-EPS|THETA-DELTA
                                     )[ \n\r]*$""", re.VERBOSE)
        numbers = re.compile(r' [ ]+([0-9]+)')
        row_num = re.compile(r'^[ ]*(KSI|ETA|VAR) (?P<rownum>[0-9]+)')
        invariant = re.compile(r'(?P<matname>[A-Z\-]{3,}) EQUALS (?P=matname) IN THE FOLLOWING GROUP[ \n\r]*$')

        free_params = [] # ngroups size list of free params

        outfile = file(outpath)
        # ngroups-length list of list of names of matrices 
        #   that were set 'invariant'
        invariant_mats = []
        for line in outfile:
            if parspec.search(line):
                in_specs = True
                igroup += 1
                invariant_mats.append([])
                free_params.append({})
                which_mat = '' # reset
                sys.stderr.write('Found specs at line %d. Group num is %d.\n' %
                        (iline, igroup))
            if in_specs:
                if end.search(line):
                    sys.stderr.write('Specs stopped at line %d\n' % iline)
                    break # stop reading output

                mat_match = matrix.search(line)
                inv_match = invariant.search(line)
                if mat_match:
                    if mat_match.group('matname') != which_mat:
                        which_mat = mat_match.group('matname')
                        short_name = self.long_names[which_mat]
                        mat_form = matforms[short_name]['Form']
                        mat_shape = self.get_matrix_shape(short_name, igroup-1)
                        cur_row = 0
                        col_start = 0
                        sys.stderr.write('Found matrix %s (%s) at line %d.\
                                \tThe matrix is %s.\n' % 
                                (which_mat, short_name, iline, mat_form))
                    else:
                        col_start += 6
                elif inv_match: # a matrix is set invariant on this line
                    invariant_mats[igroup-1].append(inv_match.group('matname'))
                    # cannot do anything yet because the free params for the
                    # next groups are not known.
                pnums = numbers.findall(line)
                if pnums:
                    rowmatch = row_num.search(line)
                    pnums = [int(x) for x in pnums]
                    if rowmatch: # FU or SY
                        cur_row = int(rowmatch.group(2))
                        for col, num in enumerate(pnums):
                            if num > 0:
                                value = "%s %d %d" % (short_name.lower(), 
                                        cur_row, col + 1 + col_start)
                                free_params[igroup-1][num] = value
                    else: # DI
                        for col, num in enumerate(pnums):
                            if num > 0:
                                cur_row = col + 1 + col_start
                                value = "%s %d %d" % (short_name.lower(), 
                                        cur_row, cur_row)
                                free_params[igroup-1][num] = value
                    if pnums:
                        sys.stderr.write('Found pnums: %s\n'%str(pnums))

            iline += 1
        sys.stderr.write('Read first %d lines from %s.\n' % (iline, outpath))

        # Now go back and fill in any invariant matrices that were found
        for igroup, inv_mats in enumerate(invariant_mats):
            for matname in inv_mats:
                short_name = self.long_names[matname].lower()
                pnums = []
                gnum = igroup
                while not pnums: # search groups until one is found w/ the params
                    gnum += 1
                    pnums = [pnum for pnum in free_params[gnum].keys() 
                             if free_params[gnum][pnum].startswith(short_name)]
                    print gnum
                for pnum in pnums:
                    free_params[igroup][pnum] = free_params[gnum][pnum]

        return free_params

    def get_derivs(self, groupnum = 2):
        "Calculate the variance-covariance matrix of the standardized estimates"
        free_params = self.get_free_params('temp/OUT')[groupnum]
        derivs = read_maxima.get_derivs('retrieve_results/derivmatrix.txt')
        D = []
        failed_keys = []
        written_keys = []
        for param in free_params.values():
            try:
                D.append(derivs[read_maxima.paramdict[param.lower()]])
                written_keys.append(param.lower())
            except KeyError:
                failed_keys.append(param.lower())
        sys.stderr.write("Failed keys: %s\n" % str(failed_keys))
        sys.stderr.write("Written keys (in order): %s\n" % str(written_keys))
        nparams = len(D)
        D = np.matrix(D)
        D.shape = (nparams, len(read_maxima.scoefdict.keys()))
        return(written_keys, D)

    def get_varcov_params(self, matname='EC', path='temp'):
        """read in the EC (Vcov matrix of the parameters)."""
        matf = file(os.path.join(path, matname+'.out'), 'rb')
        numbers = self.lisrel_science_to_other(matf.read())
        matf.close()

        nrows = nrows_symm(len(numbers))

        symat = []
        start_prev = 0
        for row in range(nrows):
            start = row + start_prev
            tmp = numbers[ start:start+row+1 ]
            tmp.extend([0.0] * (nrows - row - 1))
            symat.append(tmp)
            start_prev = start

        symat = symmetrize_matrix(np.matrix(symat))

        return(symat)

    def get_var_standardized(self, groupnum = 2, path='temp'):
        """Calculate the analytical variance-covariance matrix of the 
           standardized estimates via the Delta method for group groupnum.
           
           Note that groupnum is 0 indexed, so 2 means LISREL group 3.
           Returns a symmetric matrix of variances and covariances between the
            various standardized estimates. Which rows/columns refer to which 
            standardized estimate can be looked up in the
            dictionary read_maxima.scoefdict.
           """
        # Provide math functions when evaluating the expressions 
        #   obtained from Maxima
        from math import log, exp, sqrt

        # Varcov matrix of the parameters
        Vcov = self.get_varcov_params(path = path) 
        # key, value dict of free parameters and their parameter number
        free_params = self.get_free_params(os.path.join(path, 'OUT'))[groupnum]
        # derivative matrix and list of relevant parameters for group
        derivkeys, D = self.get_derivs(groupnum)
        # select only relevant parameters for this group from Vcov
        paramnums = []
        for paramname in derivkeys:
            try: # create a list of relevant parameter numbers as they are in Vcov
                paramnums.append(free_params.keys()\
                        [free_params.values().index(paramname)] - 1)
            except ValueError:
                pass # some relevant params are not parameters of the model
        # select only the submatrix of Vcov
        # yielded by slicing out rows and columns not in paramnums
        V = Vcov[paramnums,].T[paramnums,].T 

        # matrix estimates
        mats = self.get_matrices(path = path)

        # put matrices for this group in scope
        be = mats['BE'][groupnum]
        ly = mats['LY'][groupnum]
        te = mats['TE'][groupnum]
        ga = mats['GA'][groupnum]
        ph = mats['PH'][groupnum]
        nullify_diagonal(ph)
        ps = mats['PS'][groupnum]

        # prepare a matrix to hold the evaluated derivs
        D_e = np.matrix([0.0]*(D.shape[0]*D.shape[1]))
        D_e.shape = D.shape
        for i, val in np.ndenumerate(D):
	        D_e[i] = eval(val) # derivs are evaluated (matrices used)

        # apply Delta method:
        Vs = D_e.T * V * D_e

        return(Vs)


def symmetrize_matrix(mat):
    """mat is a NumPy.matrix or .array. Copies the lower diagonal elements
       to the upper diagonal elements."""
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            mat[i, j] = mat[j, i]
    return mat

def nullify_diagonal(mat):
    """Replaces negative numbers on the diagonal by 0.0.
       
       Sometimes variances of latent variables that are locally unidentified
       have been left free. These variances can become negative, making it
       impossible to take the sqrt(). One solution provided here is to set these
       variances to zero."""
    if mat.shape[0] != mat.shape[1]:
        raise Exception('Only square matrices can have the diagonal examined.')
    for i in range(mat.shape[0]):
        if mat[i, i] < 1e-12:
            mat[i, i] = 0.0
            sys.stderr.write('Replaced one negative number on diagonal by 0.\n')

def nrows_symm(n):
    """Calculate number of rows a symmetric matrix must have had if 
       len(vech(matrix)) equals n"""
    from math import sqrt
    return int((sqrt(8*n + 1) - 1) / 2)


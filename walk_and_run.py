#!/usr/bin/python
import os, tempfile, sys, re
from parse_lisrel import LisrelInput


def solution_obtained(outpath):
    """Checks whether the output file contains errors or non-convergence messages."""
    outfile = file(outpath, 'rb')
    outstr = outfile.read()
    outfile.close()
    if re.search(r'W_A_R_N_I_N_G: The solution has not converged',
                            outstr, re.MULTILINE):
        sys.stderr.write('No convergence!\n')
        return False
    liserrs = re.findall(r'E_R_R_O_R:([^\n\r$]+)', outstr, re.MULTILINE)
    if len(liserrs) > 0:
        sys.stderr.write('ERRORS were found:\n%s' % '\n\t'.join(liserrs))
        return False
        
    return True


def delete_hidden_dirs(dirlist):
    """Utility function to remove elements from a list of strings that start
       with a dot. These are hidden directories on *nix and windows."""
    is_hidden = map(lambda x: x.startswith('.'), dirlist)
    for entry in enumerate(is_hidden).next():
        if is_hidden[entry]:       
            del dirlist[entry]

def walk_and_run(top_dir, tempdir=''):
    """recurse through directory structure, looking for .LS8 files.
       Each .LS8 file is run.
       """
    if tempdir == '': # let tempfile library choose a tempdir by default
        tempdir = tempfile.mkdtemp()
    sys.stderr.write( "Temporary directory will be %s.\n" % 
            os.path.abspath(tempdir) )

    for dirpath, dirnames, filenames in os.walk(top_dir):
        sys.stderr.write( "Searching %s...\n" % dirpath )
        for filename in filenames:
            if filename.upper().endswith('LS8'):
                sys.stderr.write( "Found %s.\n" % filename )
                lisfile = LisrelInput(os.path.join(dirpath, filename))
                # adjust input to output matrices separately
                lisfile.write_to_file(lisfile.get_modified_input())
                try:
                    lisfile.run_lisrel(tempdir) # run lisrel to write output to tempdir
                except:
                    print "LISREL encountered an error, skipping...\n"
                    break
                if solution_obtained(os.path.join(tempdir, 'OUT')):
                    smats = lisfile.standardize_matrices()
                    for igrp in range(len(smats)):
                        for matname, stanmat in smats[igrp].iteritems():
                            print "INPUT %s, GROUP %d, MATRIX %s:" % \
                                    (filename, igrp+1, matname)
                            print stanmat
                else:
                    print "No solution could be obtained, skipping...\n"



#!/usr/bin/python
import os, tempfile, sys
from parse_lisrel import LisrelInput


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

    for dirpath, dirnames, filenames in os.walk(top_dir):
        sys.stderr.write( "Searching %s...\n" % dirpath )
        for filename in filenames:
            if filename.upper().endswith('LS8'):
                sys.stderr.write( "Found %s.\n" % filename )
                lisfile = LisrelInput(os.path.join(dirpath, filename))
                # adjust input to output matrices separately
                lisfile.write_to_file(lisfile.get_modified_input())
                lisfile.run_lisrel(tempdir) # run lisrel to write output to tempdir
                smats = lisfile.standardize_matrices()
                for igrp in range(len(smats)):
                    for matname, stanmat in smats[igrp].iteritems():
                        print "INPUT %s, GROUP %d, MATRIX %s:" % \
                                (filename, igrp+1, matname)
                        print stanmat



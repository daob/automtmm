#!/usr/bin/python
import os, tempfile, sys, re
import MySQLdb
from parse_lisrel import LisrelInput

import numpy as np
from scipy import io

epstol = np.finfo(float).eps
sys.stderr = file('logfile', 'w')


def write_tuple_to_file(tup, path, sep='\r'):
    """takes a (multidimensional) tuple and writes it to a file at path"""
    if type(path) == tuple:
       path = os.path.join(path[0], path[1])
    outfile = open(path, 'w')
    for elem in tup:
        if type(elem) == tuple:
            for subel in elem:
                outfile.write(subel + sep)
        else:
            outfile.writeline(elem)
    outfile.close()
    sys.stderr.write('Wrote tuple to file %s.\n' % path)

def solution_obtained(outpath):
    """Checks whether the output file contains errors or non-convergence 
       messages."""
    outfile = file(outpath, 'rb')
    outstr = outfile.read()
    outfile.close()
    if re.search(r'W_A_R_N_I_N_G: The solution has not converged',
                            outstr, re.MULTILINE) or \
                 re.search(r'W_A_R_N_I_N_G: Serious problems were encountered',
                            outstr, re.MULTILINE):
        sys.stderr.write('No convergence!\n')
        return False
    liserrs = re.findall(r'E_R_R_O_R:([^\n\r$]+)', outstr, re.MULTILINE)
    if len(liserrs) > 0:
        sys.stderr.write('ERRORS were found:\n%s' % '\n\t'.join(liserrs))
        return False
        
    return True


def default_action(matrix, **kwargs):
    """By default the standardized matrices encountered by walk_and_run are 
       just printed"""
    print matrix


def save_estimates(input_path, experiment, country, study, val, rel, met, 
        varnum, update_or_insert = 'insert'):
    """Writes one row of estimates data to the database. Returns True if all
       is well, False if an exception occurs (exception is not thrown 
       directly to ensure that the database connection is closed)."""
    try:
        conn = MySQLdb.connect (host = "localhost",
                               user = "automtmm",
                               passwd = "automtmm",
                               db = "automtmm")
    except MySQLdb.Error, e:
        sys.stderr.write( "MySQL error %d: %s\n" % (e.args[0], e.args[1]))
        return False
    cursor = conn.cursor()
    try:
        if update_or_insert == 'insert':
            sql = """INSERT INTO estimates (input_path, experiment, country, 
                    study, validity_coef, reliability_coef, method_coef, 
                    var_num ) VALUES
                        ('%s', '%s', '%s', '%s', %2.16f, %2.16f, %2.16f, %d)
                    """ % (input_path, experiment, country, study, val, rel, 
                            met, varnum) 
        elif update_or_insert == 'update':
            sql = """UPDATE estimates SET reliability_coef=%2.16f
                     WHERE
                        input_path='%s' and experiment='%s' and country='%s' 
                    and study='%s' and var_num=%d """ % (rel, input_path, 
                        experiment, country, study, varnum) 
            
        sys.stderr.write(sql + "\n")
        cursor.execute(sql)
        conn.commit()
        
    except MySQLdb.Error, e:
        sys.stderr.write( "MySQL error %d: %s\n" % (e.args[0], e.args[1]))
        return False
    finally:
        conn.close()
    return True

def entry_exists(input_path, experiment, country, study, varnum):
    """Checks whether the entry with the given characteristics 
       is already in the database."""
    try:
        conn = MySQLdb.connect (host = "localhost",
                               user = "automtmm",
                               passwd = "automtmm",
                               db = "automtmm")
    except MySQLdb.Error, e:
        sys.stderr.write( "MySQL error %d: %s\n" % (e.args[0], e.args[1]))
        return False
    cursor = conn.cursor()
    try:
        sql = """SELECT * FROM estimates WHERE
                        input_path='%s' and experiment='%s' and country='%s' and
                        study='%s' and var_num=%d
                    """ % (input_path, experiment, country, study, varnum) 
        sys.stderr.write(sql + "\n")
        cursor.execute(sql)
        if cursor.fetchone():
            return True
    except MySQLdb.Error, e:
        sys.stderr.write( "MySQL error %d: %s\n" % (e.args[0], e.args[1]))
    finally:
        conn.close()
    return False

                    
def retrieve_mtmm(matrix, **kwargs):
    """An 'action' that collects the reliabilities, validities, and method 
       effects and writes them to one data file."""
    group_num = kwargs['group_num']
    dirpath = kwargs['dirpath']
    filename = kwargs['filename']
    path = os.path.splitext(dirpath)[0].split(os.sep)[-3:]
    experiment = path[-1]
    country = path[-2]
    study = path[-3]
    sys.stderr.write("Called retrieve_mtmm:\n\tdirpath: %s\n\tfilename: %s\n\t\
group: %d\n\texperiment: %s\n\tcountry: %s\n\tstudy: %s\n\n" % \
        (dirpath,filename,group_num,experiment,country,study))
    
    #nrows = matrix.shape[0]
    input_path = os.path.join(dirpath, filename)
    rows = range(3); rows.extend(map(lambda x: x+group_num*3, range(3)))
    for irow in rows: # loop only over variables that were observed in this group
        if kwargs['matname'] == 'GA':
            val, met = matrix[[irow, irow],[irow%3, (irow + 3)/3 + 2]].tolist()[0]
            if entry_exists(input_path, experiment, country, study, irow):
                res = save_estimates(input_path, 
                    experiment, country, study, val, -9.0, met, irow, 'update')
            else:
                res = save_estimates(input_path, 
                    experiment, country, study, val, -9.0, met, irow, 'insert')
        if kwargs['matname'] == 'LY':
            rel = matrix[irow, irow]
            if entry_exists(input_path, experiment, country, study, irow):
                res = save_estimates(os.path.join(dirpath, filename), 
                    experiment, country, study, -9.0, rel, -9.0, irow, 'update')
            else:
                res = save_estimates(os.path.join(dirpath, filename), 
                    experiment, country, study, -9.0, rel, -9.0, irow, 'insert')


def walk_and_run(top_dir, tempdir='', action=default_action):
    """recurse through directory structure, looking for .LS8 files.
       Each .LS8 file is run.
       """
    if tempdir == '': # let tempfile library choose a tempdir by default
        tempdir = tempfile.mkdtemp()
    sys.stderr.write( "Temporary directory will be %s.\n" % 
            os.path.abspath(tempdir) )
    top_dir = os.path.abspath(top_dir)
    not_converged = file('not_converged', 'w')

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
                finally:
                    if os.path.exists(lisfile.path + '.backup'):
                        os.remove(lisfile.path)
                        os.rename(lisfile.path + '.backup', lisfile.path)
                    else:
                        sys.stderr.write('WARNING: Could not restore backup LS8 file.\n')
                if solution_obtained(os.path.join(tempdir, 'OUT')):
                    smats = lisfile.standardize_matrices()
                    for igrp in range(len(smats)):
                        for matname, stanmat in smats[igrp].iteritems():
                            sys.stderr.write( "INPUT %s, GROUP %d, MATRIX %s:" % \
                                    (filename, igrp+1, matname))
                            action(stanmat, matname=matname, group_num = igrp+1,
                                    filename=filename, dirpath=dirpath)
                    # try to write the variance matrix of 
                    #   the standardized estimates
                    try:
                        vnames, vmat = lisfile.get_var_standardized(path = \
                                tempdir)
                        vfile = open(os.path.join(dirpath, 
                                    'vcov_standardized.txt'), 'w')
                        io.write_array(vfile, vmat, separator='\t',
                                    linesep='\n', precision=10,) # closes vfile
                        write_tuple_to_file(vnames, 
                                    path=(dirpath, 'vcov_standardized.names'))
                    except:
                        sys.stderr.write('ERROR writing or getting vcov matrix of standardized estimates for group %d. Error: %s\n' % (igrp, str(e.args)))
                else:
                    print "No solution could be obtained, skipping...\n"
                    not_converged.write(os.path.join(dirpath, filename) + "\n")

    not_converged.close()

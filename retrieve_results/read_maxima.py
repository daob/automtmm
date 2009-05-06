#!/usr/bin/python

import os, re


def pythonize_maxima(maxpath='derivmatrix.txt'):
    """Read in Maxima file which contains the analytic expressions for the first
       derivatives of the standardized estimates w.r.t. the parameters and convert it 
       into a Python expression that can be evaluated.
       Returns string that will evaluate to a list of strings to be evaluated.
       """
    der_file = open(maxpath, 'rb')

    linesep = re.compile(r'-9[\n\r]', re.MULTILINE)
    commasep = re.compile(r'([^,\[\]]+)([,\]])', re.MULTILINE)
    number = re.compile(r'(?<![a-z0-9])([0-9]+)', re.MULTILINE)
    powerop = re.compile(r'\^', re.MULTILINE)
    index = re.compile(r'([a-z]{2})([0-9]{1,2})([0-9])', re.MULTILINE)

    der_str = der_file.read()
    der_str = linesep.sub(r'], \n[', der_str) # recognize rows
    der_str = commasep.sub(r"r'\1'\2", der_str) # make list of strings to be evaluated
    der_str = number.sub(r'\1.0', der_str) # make numbers floats
    der_str = powerop.sub(r'**', der_str)  # maxima uses ^ while python uses ** for powers
    der_str = index.sub(r'\1[\2-1,\3-1]', der_str)  # indexing from ga11 to ga[0,0]
    der_str = '[' + der_str[2:-2] + ']' # enclose in list constructor, remove beg & end
    der_str = der_str.replace('\n', ' ') # remove newlines
    der_str = der_str.replace('],', '],\n') # newlines between list elts
    der_str = der_str.replace('\',', '\',\n') # newlines between list elts

    return der_str

def get_derivs(maxpath='derivmatrix.txt'):
    """Use pythonize_maxima() to obtain a list of lists of strings to be evaluated.
       Returns a list 'derivs'.

       Each list in derivs refers to the first derivatives wrt to one free parameter.
       Each string in each of these lists refers to one standardized coefficient.
          (the order for both of these can be found in the maxima .mac input file).
       The string can be evaluated in an environment where the relevant matrices are
            present as NumPy.matrices or arrays. Also 'from math import sqrt' is needed."""
    derivs = eval(pythonize_maxima(maxpath))

    return derivs

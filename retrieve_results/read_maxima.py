"""
This module consists of two parts: one written in the Maxima Computer 
Algebra System language <http://maxima.sourceforge.net/>, and the other a Python
script to read in and translate the results obtained from Maxima to Python.

In the Maxima script, the standardized gamma and lambda coefficients are 
first defined in terms of the unstandardized parameters.
These parameters *might*, but need not be, free parameters of the 
model for a given MTMM analysis.

The analytical derivatives of the standardized coefficients are then taken 
for each parameter. This yields a (number of parameters) x (number coefficients)
size matrix of analytical expressions in terms of the parameters.

This matrix is read in by the Python script and used by the ``parse_lisrel``
module to calculate the variance-covariance matrix of the standardized 
coefficients. 

See also the ``get_var_standardized`` function in ``parse_lisrel``.
"""
#!/usr/bin/python

import os, re, sys

paramdict = {'ph 1 1' : 0, 'ph 2 2' : 1, 'ph 3 3' : 2,
'ph 4 4' : 3, 'ph 5 5' : 4, 'ph 6 6' : 5, 'ph 7 7' : 6,
'ph 2 1' : 7, 'ph 3 2' : 8, 'ph 3 1' : 9, 'ga 1 1' : 10,
'ga 1 4' : 11, 'ga 2 2' : 12, 'ga 2 4' : 13, 'ga 3 3' : 14,
'ga 3 4' : 15, 'ga 4 1' : 16, 'ga 4 5' : 17, 'ga 5 2' : 18,
'ga 5 5' : 19, 'ga 6 3' : 20, 'ga 6 5' : 21, 'ga 7 1' : 22,
'ga 7 6' : 23, 'ga 8 2' : 24, 'ga 8 6' : 25, 'ga 9 3' : 26,
'ga 9 6' : 27, 'ga 10 1' : 28, 'ga 10 7' : 29, 'ga 11 2' : 30,
'ga 11 7' : 31, 'ga 12 3' : 32, 'ga 12 7' : 33, 

'te 1 1' : 34, 'te 2 2' : 35, 'te 3 3' : 36, 'te 4 4' : 37,
'te 5 5' : 38, 'te 6 6' : 39, 'te 7 7' : 40, 'te 8 8' : 41,
'te 9 9' : 42, 'te 10 10' : 43, 'te 11 11' : 44, 'te 12 12' : 45,
} 

scoefdict = {'ga 1 1':0, 'ga 2 2':1, 'ga 3 3':2, 'ga 4 1':3,
'ga 5 2':4, 'ga 6 3':5, 'ga 7 1':6, 'ga 8 2':7,
'ga 9 3':8, 'ga 10 1':9, 'ga 11 2':10, 'ga 12 3':11,
'ga 1 4':12, 'ga 2 4':13, 'ga 3 4':14, 'ga 4 5':15,
'ga 5 5':16, 'ga 6 5':17, 'ga 7 6':18, 'ga 8 6':19,
'ga 9 6':20, 'ga 10 7':21, 'ga 11 7':22, 'ga 12 7':23,

'ly 1 1' : 24, 'ly 2 2' : 25, 'ly 3 3' : 26, 'ly 4 4' : 27,
'ly 5 5' : 28, 'ly 6 6' : 29, 'ly 7 7' : 30, 'ly 8 8' : 31,
'ly 9 9' : 32, 'ly 10 10' : 33, 'ly 11 11' : 34, 'ly 12 12' : 35,
}


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
    index = re.compile(r'([a-z]{2})([0-9]{1,2})([0-9]{1,2})', re.MULTILINE)

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
       (the order is in paramdict)

       Each string in each of these lists refers to one standardized coefficient.
       (the order is in scoefdict and also in the handy-to-read scoefs.names file
       which can be read by R scan() )
     
       The string can be evaluated in an environment where the relevant matrices are
       present as NumPy.matrices or arrays. Also 'from math import sqrt' is needed."""
    derivs = eval(pythonize_maxima(maxpath))

    return derivs




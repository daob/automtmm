#!/usr/bin/python
import re
from copy import deepcopy


def get_matrix_forms(input):
    """Retrieve 'form' (full, symmetrix, zero, diagonal, ... and free or fixed) 
       Of matrices for LISREL model for each group.
       Returns an <ngroups> list of dictionaries."""

    mats = { 'LY': {'Form':'FU', 'Free':'FI'},
         'LX': {'Form':'FU', 'Free':'FI'}, 
         'TE': {'Form':'DI', 'Free':'FR'}, 
         'TD': {'Form':'DI', 'Free':'FR'}, 
         'BE': {'Form':'ZE', 'Free':'FI'}, 
         'GA': {'Form':'FU', 'Free':'FR'}, 
         'PH': {'Form':'SY', 'Free':'FR'}, 
         'PS': {'Form':'DI', 'Free':'FR'}, 
         'TY': {'Form':'DI', 'Free':'FI'}, 
         'TX': {'Form':'DI', 'Free':'FI'}, 
         'KA': {'Form':'DI', 'Free':'FI'}, 
         'AL': {'Form':'DI', 'Free':'FI'} }

    ng = get_ngroups(input)
    forms = []
    start_re = r'^[ \t]*MO[A-Z0-9=, \t]+'

    for ig in range(ng):
        forms.append(deepcopy(mats))
    
        for n in mats.keys():
            find_n = start_re + n + r'[ ]*=[ ]*([A-Z,]+)'
            find = re.findall(find_n, input, re.MULTILINE | re.IGNORECASE)
            if len(find) > 0:
                tmp = find[ig].split(',')
                if len(tmp) > 1:
                    forms[ig][n]['Form'] = tmp[0].upper()
                    forms[ig][n]['Free'] = tmp[1].upper()
                elif tmp[0].upper() == 'IN':
                    forms[ig][n]['Form'] = forms[ig - 1][n]['Form']
                    forms[ig][n]['Free'] = 'IN'
    return(forms)

def get_ngroups(input):
    "Retrieve number of groups. Fails if file contains stacked analyses."
    model_line = r'^[ \t]*MO[^N]+'
    res = re.findall(model_line, input, re.MULTILINE | re.IGNORECASE)
    return(len(res))


def get_dimensions(input):
    """Retrieve number of x, y, eta, and ksi variables for each group.
       Returns a <ngroups> list of dictionaries."""

    ng = get_ngroups(input)
    dims = []
    ns = {'NX':0, 'NY':0, 'NE':0, 'NK':0}
    start_re = r'^[ \t]*MO[A-Z0-9=, \t]+'
    for ig in range(ng):
        dims.append(deepcopy(ns))
    
        for n in ns.keys():
            find_n = start_re + n + r'[ ]*=[ ]*([0-9]+)'
            find = re.findall(find_n, input, re.MULTILINE | re.IGNORECASE)
            if len(find) > 0:
                dims[ig][n] = int(find[ig])
    return(dims)

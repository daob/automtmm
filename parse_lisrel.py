#!/usr/bin/python
import re


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
         'AL': {'Form':'DI', 'Free':'FI'} 
        }

def get_ngroups(input):
    model_line = r'^[ \t]*MO[^N]+'
    res = re.findall(model_line, input, re.MULTILINE | re.IGNORECASE)
    return(len(res))


def get_dimensions(input):
    from copy import deepcopy

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

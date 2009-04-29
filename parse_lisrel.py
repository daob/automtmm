"""Classes to deal with LISREL input and output files."""
#!/usr/bin/python
import re
from copy import deepcopy


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
        self.mats = { 'LY': {'Form':'FU', 'Free':'FI'},
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
        """Modifies input to write matrix results to files. Returns string."""
        outstr = ' '.join(["%s=%s.out"%(key, key) for key in self.mats.keys()])
        reg_out = re.compile(r'^[ ]*OU([A-Z0-9=.\'"]+)', self.re_flags)
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

"""Python class to read in and parse LISREL model files from output."""

import re
from Group import Group
from Helpers import lf


class LisrelModel(object):
    """A LISREL model containing groups containing matrices. LISREL output
    parsing and convenience functions."""

    # This one strips whitespace but involves too much backtracking leading to
    # 3 times longer execution time:
    #re_std = re.compile(r"(?P<group>[\w \)\(\-\!]+?)[ ]+[\n\r ]+Within Group Completely Standardized Solution[ ]*[\n\r](?P<std_txt>.+?)Correlation Matrix of ETA and KSI", re.DOTALL)
    re_std = re.compile(r"([\w \)\(\-\!]+)[\n\r ]+Within Group Completely Standardized Solution[ ]*[\n\r](.+?)Correlation Matrix of ETA and KSI", re.DOTALL)

    re_group = re.compile(r"[\n\r][ ]+Number of Groups[ ]+(\d+)[ ]*[\n\r]")

    # List of groups detected in this model output
    groups = []

    def __init__(self, path):
        self.path = path
        outfile = open(path, 'rb')
        self.txt = lf(outfile.read())
        outfile.close()

        self.ngroups = self.get_ngroups()

    def __repr__(self):
        return "Model file '%s'" % (self.path)

    def get_ngroups(self):
        """Read in number of groups from the LISREL output file."""
        match = self.re_group.search(self.txt)
        if not match:
            raise Exception("Could not read number of groups. Please check "
                "that this is a valid LISREL file.")

        return int(match.group(1))

    def create_groups_from_std(self):
        """Given the output text, use the regular expression re_std to split
        the within-group standardized matrix output into groups, detect
        groups, and create groups, adding them to self.groups.
        """
        self.re_std_result = self.re_std.findall(self.txt)
        self.groups = [] # Clear any existing group list

        # Loop over results and add a new Group for each detected group
        for igroup, group in enumerate(self.re_std_result):
            newgroup = Group(group[0].strip(), igroup + 1)
            #import pdb; pdb.set_trace()
            newgroup.create_matrices(group[1])
            self.groups.append(newgroup)



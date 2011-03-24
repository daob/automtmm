"""Python class to read in and parse LISREL model files from output."""

import re


class LisrelModel(object):
    """A LISREL model containing groups containing matrices. LISREL output
    parsing and convenience functions."""

    re_std = re.compile(r"(?P<group>[\w \)\(\-\!]+?)[ ]+[\n\r ]+Within Group Completely Standardized Solution[ ]*[\n\r](?P<std_txt>.+?)Correlation Matrix of ETA and KSI", re.DOTALL)

    re_group = re.compile(r"[\n\r][ ]+Number of Groups[ ]+(\d+)[ ]*[\n\r]")

    def __init__(self, path):
        self.path = path
        outfile = open(path, 'rb')
        self.txt = outfile.read()
        outfile.close()

        self.ngroups = self.get_ngroups()

    def get_ngroups(self):
        """Read in number of groups from the LISREL output file."""
        match = self.re_group.search(self.txt)
        if not match:
            raise Exception("Could not read number of groups. Please check "
                "that this is a valid LISREL file.")

        return int(match.group(1))

#! /usr/bin/python2.7

import sys
import argparse
import json
import LisrelModel


def setup(path):
    mod = LisrelModel.LisrelModel(path)
    mod.create_groups_from_std()

    return mod

def output_json(args):
    mod = setup(args.input)
    out = args.output and open(args.output, 'w') or sys.stdout

    outlist = []
    for group in mod.groups:
        for matrix in group.matrices:
            for i in range(matrix.nrows):
                for j in range(matrix.ncols):
                    val = matrix.values_std[i][j]

                    if not abs(val) > 1e-6: continue

                    outlist.append({'group_name':group.name,
                        'group_num':group.number,
                        'parameter':"%s %d %d" % (matrix.short_name, i+1, j+1),
                        'row':i+1, 'col':j+1, 'matrix':matrix.name,
                        'value_std':val
                        })

    jout = json.dumps(outlist)
    out.write(jout)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    parser.add_argument('-o', '--output')
    parser.add_argument('-m', '--matrix')
    parser.add_argument('-g', '--groups')
    parser.add_argument('-v', dest='verbose', action='store_true')
    args = parser.parse_args()

    output_json(args)

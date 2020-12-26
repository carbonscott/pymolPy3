#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymolPy3
import argparse
import os

parser = argparse.ArgumentParser(
description = 
"""Visualize a chain of rhodopsin with each transmembrane selected."""
,formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument(
    'pdb_chain', 
    metavar = 'pdb chain', 
    nargs   = 2, 
    help    = 'Specify the pdb and chain to visualize.')
parser.add_argument(
    'drc', 
    metavar = 'directory', 
    help    = 'Specify the directory containing the pdb file.')
args = parser.parse_args()


# Set the input parameters...
pdb, chain = args.pdb_chain
fl_pdb     = f"{pdb}.pdb"
drc        = args.drc
pdb_path   = os.path.join(drc, fl_pdb)

# Define the transmembrane regions...
TMs     = {"TM1"  : [ 33,  65],
           "TM2"  : [ 70, 100],
           "TM3"  : [105, 140],
           "TM4"  : [149, 173],
           "TM5"  : [199, 226],
           "TM6"  : [240, 277],
           "TM7"  : [288, 307],
           "H8"   : [310, 322]}

pm = pymolPy3.pymolPy3()
pm(f"load {pdb_path}")
pm(f"remove not chain {chain}")
pm(f"spectrum")
pm(f"orient chain {chain}")
for k in TMs.keys():
    tm = k
    resi = TMs[tm]
    pm(f"select {tm}, chain {chain} and (resi {resi[0]}-{resi[1]})")
    pm(f"disable {tm}")
input("Press Enter to exit...")

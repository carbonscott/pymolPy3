#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pyrotein as pr
import pymolPy3
from loaddata import load_xlsx
import os

# Load template...
template_pdb = 'template.pdb'
template_list = pr.atom.read(template_pdb)
template_dict = pr.atom.create_lookup_table(template_list)

# Specify chains to process...
fl_chain = "chains.comp.xlsx"
lines    = load_xlsx(fl_chain)
drc      = "pdb"

# Specify the segment....
peptide = ["N", "CA", "C", "O"]
nterm   = 1
cterm   = 322
len_chain = (cterm - nterm + 1) * len(peptide)

# Accumulate coordinates from each chain...
xyzs = np.zeros( (len(lines), len_chain, 3) )
for i_fl, line in enumerate(lines):
    # Unpack parameters
    _, pdb, chain, species = line[:4]

    # Read coordinates from a PDB file...
    fl_pdb    = f"{pdb}_{chain}.align.pdb"
    pdb_path  = os.path.join(drc, fl_pdb)
    atoms_pdb = pr.atom.read(pdb_path)

    # Create a lookup table for this pdb...
    atom_dict = pr.atom.create_lookup_table(atoms_pdb)

    # Obtain coordinates...
    xyzs[i_fl, :, :] = pr.atom.extract_xyz(peptide, atom_dict, chain, nterm, cterm)

# Obtain the mean matrix...
xyzs_mean = np.nanmean(xyzs, axis = 0)

# Launch pymol
pm = pymolPy3.pymolPy3(0)
pm(f"load {template_pdb}")
i_acc = 0
for i, resi in enumerate(range(nterm, cterm + 1)):
    for j, name in enumerate(peptide):
        # Update the coordinates...
        x, y, z = xyzs_mean[i_acc]

        # Alter the template structure...
        pm(f"alter_state 1, (resi {resi} and name {name}), (x, y, z) = ({x}, {y}, {z})")

        i_acc += 1

pm(f"save average.pdb, all")

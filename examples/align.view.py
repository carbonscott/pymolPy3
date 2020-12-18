#!/usr/bin/env python3
# -*- coding: utf-8 -*-

''' Align a list of molecules using `super` command in PyMol.  The first item 
    in the list is considered as the reference.  
'''

import pymolPy3
import pyrotein as pr
import os

# Specify chains to process...
fl_chain = "chains.comp.dat"
lines    = pr.utils.read_file(fl_chain)
drc      = "pdb_vr"

# Define atoms used for distance matrix analysis...
peptide = ["N", "CA", "C", "O"]

# Specify the range of atoms from rhodopsin...
nterm = 1
cterm = 348
len_atoms_peptide = (cterm - nterm + 1) * len(peptide)

# Specify the rigid framework...
fl_fwk     = 'fwk.dat'
fwk        = pr.utils.read_file(fl_fwk)
fwk_select = ' or '.join( [ f"(resi {'-'.join(i)})" for i in fwk ] )

# Start pymol
pm = pymolPy3.pymolPy3()
pm("bg white")

# Load the first structure (target)...
pdb, chain = lines[0]
entry  = f"{pdb}_{chain}.align"
pdb_path   = os.path.join(drc, f"{entry}.pdb")
pm(f"load {pdb_path}")

# Select the rigid framework from the target...
target = f"{entry}_fwk"
pm(f"select {target}, %{entry} and ({fwk_select})")
pm(f"disable %{target}")

# Go through each mobile
for line in lines[1:]:
    # Load a mobile structure...
    pdb, chain = line
    entry  = f"{pdb}_{chain}.align"
    pdb_path   = os.path.join(drc, f"{entry}.pdb")
    pm(f"load {pdb_path}")

    # Select the rigid framework from the mobile...
    mobile = f"{entry}_fwk"
    pm(f"select {mobile}, %{entry} and ({fwk_select})")
    pm(f"disable %{mobile}")
pm(f"select fwk, all and ({fwk_select})")
pm(f"disable %fwk")




# Customization
# Set view...
pm("set_view (\\")
pm("     0.796704233 ,   -0.603343129,    0.035119072,\\")
pm("    -0.342249423 ,   -0.402523756,    0.849020958,\\")
pm("    -0.498112202 ,   -0.688440979,   -0.527183950,\\")
pm("    -0.000300951 ,   -0.000151135, -243.658477783,\\")
pm("    58.718177795 ,    8.645618439,   -0.894862056,\\")
pm("  -1408.164916992, 1895.492553711,  -20.000000000  )")

# Set the lighting...
pm("set ambient           , 0.05")
pm("set direct            , 0.2" )
pm("set spec_direct       , 0"   )
pm("set shininess         , 10." )
pm("set reflect           , 0.5" )
pm("set spec_count        , -1"  )
pm("set spec_reflect      , -1." )
pm("set specular          , 1"   )
pm("set specular_intensity, 0.5" )

# Hide the non-rhodopsin region...
pm(f"hide cartoon, (not resi {nterm}-{cterm})")

# Customize the 
pm(f"set cartoon_color, 0x4C62D2, %fwk")
pm(f"set cartoon_transparency, 0.6, %fwk")
pm(f"set cartoon_transparency, 0.8, not %fwk")

# Export...
## pm("ray 1497, 1600, async=1")
pm("draw 1497, 1600")
pm("png align.view.png")
input("Press Enter to exit...")

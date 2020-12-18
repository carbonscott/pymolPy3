#!/usr/bin/env python3
# -*- coding: utf-8 -*-

''' Visualize the aligned rhodopsin structures based on the rigid framework
    specified in `fwk.dat`

    The chains to align are specified in `chains.comp.dat`.  

    PDBs files are save under `pdb_vr` directory.  
'''

import pymolPy3
import os

def read_file(file, numerical = False):
    '''Return all lines in the user supplied parameter file without comments.
    '''
    lines = []
    with open(file,'r') as fh:
        for line in fh.readlines():
            # Separate entries by spaces and remove commented lines...
            words = line.replace('#', ' # ').split()

            # Omit any thing coming after the pound sign in a line...
            if "#" in words: words = words[  : words.index("#")]

            # Save non-empty line...
            if numerical: words = [ float(word) for word in words ]
            if len(words) > 0: lines.append(words)

    return lines

# Specify chains to process...
fl_chain = "chains.comp.dat"
lines    = read_file(fl_chain)
drc      = "pdb_vr"

# Specify the range of atoms from rhodopsin...
nterm = 1
cterm = 348

# Specify the rigid framework...
fl_fwk     = 'fwk.dat'
fwk        = read_file(fl_fwk)
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
pm("set 'ambient'           , 0.05")
pm("set 'direct'            , 0.2" )
pm("set 'spec_direct'       , 0"   )
pm("set 'shininess'         , 10." )
pm("set 'reflect'           , 0.5" )
pm("set 'spec_count'        , -1"  )
pm("set 'spec_reflect'      , -1." )
pm("set 'specular'          , 1"   )
pm("set 'specular_intensity', 0.5" )

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

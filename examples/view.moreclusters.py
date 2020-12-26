#!/usr/bin/env python3
# -*- coding: utf-8 -*-

''' Align a list of molecules using `super` command in PyMol.  The first item 
    in the list is considered as the reference.  
'''

import pymolPy3
import pyrotein as pr
import os
import colorsimple as cs
from loaddata import load_xlsx

# Specify chains to process...
fl_chain = "chains.comp.xlsx"
lines    = load_xlsx(fl_chain)
drc      = "pdb"

# Define atoms used for distance matrix analysis...
peptide = ["N", "CA", "C", "O"]

# Specify the range of atoms from rhodopsin...
nterm = 1
cterm = 348
len_atoms_peptide = (cterm - nterm + 1) * len(peptide)

# Start pymol
pm = pymolPy3.pymolPy3()
## pm("bg white")

# Get the color palette...
color_items = [ i[4] for i in lines ]
spe         = { i : 0 for i in color_items }.keys()
color_dict  = cs.color_species(spe, hexsym = '0x')

# Go through each mobile
custom_clusters = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 26, 27, 31, 32, 66, 67]

entries = []
for i in custom_clusters:
    # Unpack parameters
    _, pdb, chain, _, chrome = lines[i][:5]

    # Load a mobile structure...
    entry    = f"{pdb}_{chain}.align"
    pdb_path = os.path.join(drc, f"{entry}.pdb")
    pm(f"load {pdb_path}")

    # Show cartoon and custom it...
    pm(f"hide cartoon, %{entry}")
    pm(f"set cartoon_color, {color_dict[chrome]}, %{entry}")

    # Set ribbon color...
    pm(f"show ribbon, %{entry}")
    ## pm(f"set ribbon_color, {color_dict[chrome]}, %{entry}")
    pm(f"set ribbon_color, blue, %{entry}")

    entries.append(entry)

pm(f"select cluster1, {' or '.join(entries)}")
pm(f"disable %cluster1")


custom_clusters = [25, 28, 29, 30, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 68, 69, 70, 71, 72, 73]

entries = []
for i in custom_clusters:
    # Unpack parameters
    _, pdb, chain, _, chrome = lines[i][:5]

    # Load a mobile structure...
    entry  = f"{pdb}_{chain}.align"
    pdb_path   = os.path.join(drc, f"{entry}.pdb")
    pm(f"load {pdb_path}")

    # Show cartoon and custom it...
    pm(f"hide cartoon, %{entry}")
    pm(f"set cartoon_color, {color_dict[chrome]}, %{entry}")

    # Set ribbon color...
    pm(f"show ribbon, %{entry}")
    ## pm(f"set ribbon_color, {color_dict[chrome]}, %{entry}")
    pm(f"set ribbon_color, green, %{entry}")

    entries.append(entry)

pm(f"select cluster2, {' or '.join(entries)}")

pm(f"disable %cluster2")

# Customization

# Set view...
pm("set_view (\\")
pm("     0.796704233 ,   -0.603343129,    0.035119072,\\")
pm("    -0.342249423 ,   -0.402523756,    0.849020958,\\")
pm("    -0.498112202 ,   -0.688440979,   -0.527183950,\\")
pm("    -0.000300951 ,   -0.000151135, -243.658477783,\\")
pm("    58.718177795 ,    8.645618439,   -0.894862056,\\")
pm("  -1408.164916992, 1895.492553711,  -20.000000000  )")

## # Set the lighting...
## pm("set ambient           , 0.05")
## pm("set direct            , 0.2" )
## pm("set spec_direct       , 0"   )
## pm("set shininess         , 10." )
## pm("set reflect           , 0.38" )
## pm("set spec_count        , -1"  )
## pm("set spec_reflect      , -1." )
## pm("set specular          , 1"   )
## pm("set specular_intensity, 0.5" )

# Hide the non-rhodopsin region...
pm(f"hide cartoon, (not resi {nterm}-{cterm})")
pm(f"hide ribbon, (not resi {nterm}-{cterm})")

## # Hide retinal...
## pm(f"hide everything, resn ret")

# Export...
input("Press Enter to exit...")
## pm("ray 1497, 1600, async=1")
## pm("draw 4491, 6400")
## pm("png align.view.png")

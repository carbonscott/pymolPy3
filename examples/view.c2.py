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
cterm = 322
len_peptide = (cterm - nterm + 1) * len(peptide)

# Start pymol
pm = pymolPy3.pymolPy3()
## pm("bg white")

# Get the color palette...
color_items = [ i[4] for i in lines ]
spe         = { i : 0 for i in color_items }.keys()
color_dict  = cs.color_species(spe, hexsym = '0x')

# Define the transmembrane regions...
TMs     = {"TM1"  : [ 33,  65],
           "ICL1" : [ 66,  69],
           "TM2"  : [ 70, 100],
           "ECL1" : [101, 104],
           "TM3"  : [105, 140],
           "ICL2" : [141, 148],
           "TM4"  : [149, 173],
           "ECL2" : [174, 198],
           "TM5"  : [199, 226],
           "ICL3" : [227, 239],
           "TM6"  : [240, 277],
           "ECL3" : [278, 287],
           "TM7"  : [288, 307],
           "L78"  : [308, 309],
           "H8"   : [310, 322] }

# Choose the select to show colors...
disp_range = [33, 322]
color_clusters = [ str(i) for i in range(disp_range[0],disp_range[1] + 1) ]




# [[[ cluster 1 -- active ]]]
# Go through each structure
custom_clusters = [25, 28, 29, 30, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45,
         46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62,
         63, 64, 65, 68, 69, 70, 71, 72, 73]

# Define custom color
custom_color = {
    "active"   : "0xffa600",
    "inactive" : "0x003f5c",
    "average"  : "0xffd1ff",
}

entries = []
for i in custom_clusters[:]:
    # Unpack parameters
    _, pdb, chain, _, chrome = lines[i][:5]

    # Load a mobile structure...
    entry    = f"{pdb}_{chain}.align"
    pdb_path = os.path.join(drc, f"{entry}.pdb")
    pm(f"load {pdb_path}")

    entries.append(entry)

pm(f"select cluster1, ({' or '.join(entries)}) and (resi {nterm}-{cterm})")
pm(f"select cluster_active, %cluster1 and resi {'+'.join(color_clusters)}")
pm(f"select ret_active, ({' or '.join(entries)}) and resn ret")
pm(f"select hoh_active, ({' or '.join(entries)}) and resn hoh")
pm(f"disable %cluster1")
pm(f"disable %cluster_active")
pm(f"disable %ret_active")
pm(f"disable %hoh_active")

# The appearance of TMs in cluster1...
# Cartoon of TMs
pm(f"hide cartoon, %cluster1")
pm(f"set cartoon_color, white, %cluster1")

# Ribbon of TMs
pm(f"show ribbon, %cluster1")
pm(f"set ribbon_color, white, %cluster1")

# Set the water representation...
pm(f"hide everything, %hoh_active")
pm(f"show sphere, %hoh_active")
pm(f"set sphere_color, {custom_color['active']}, %hoh_active")

# Color specific region to inactive color...
pm(f"set ribbon_color, {custom_color['active']}, %cluster1 and resi {'+'.join(color_clusters)}")
pm(f"set cartoon_color, {custom_color['active']}, %cluster1 and resi {'+'.join(color_clusters)}")
pm(f"set stick_color, {custom_color['active']}, %ret_active and resn ret")




# [[[ cluster 2 -- inactive ]]]
custom_clusters = [0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16,
         17, 18, 19, 20, 21, 22, 23, 24, 26, 27, 31, 32, 66, 67]

entries = []
for i in custom_clusters[:]:
    # Unpack parameters
    _, pdb, chain, _, chrome = lines[i][:5]

    # Load a mobile structure...
    entry  = f"{pdb}_{chain}.align"
    pdb_path   = os.path.join(drc, f"{entry}.pdb")
    pm(f"load {pdb_path}")

    entries.append(entry)

pm(f"select cluster2, ({' or '.join(entries)}) and (resi {nterm}-{cterm})")
pm(f"select cluster_inactive, %cluster2 and resi {'+'.join(color_clusters)}")
pm(f"select ret_inactive, ({' or '.join(entries)}) and resn ret")
pm(f"select hoh_inactive, ({' or '.join(entries)}) and resn hoh")
pm(f"disable %cluster2")
pm(f"disable %cluster_inactive")
pm(f"disable %ret_inactive")
pm(f"disable %hoh_inactive")

pm(f"select cluster_gray, (%cluster1 or %cluster2) and not (%cluster_active or %cluster_inactive)")
pm(f"disable %cluster_gray")


# The appearance of cluster2
# Cartoon of TMs
pm(f"hide cartoon, %cluster2")
pm(f"set cartoon_color, white, %cluster2")

# Ribbon of TMs
pm(f"show ribbon, %cluster2")
pm(f"set ribbon_color, white, %cluster2")

# Set the water representation...
pm(f"hide everything, %hoh_inactive")
pm(f"show sphere, %hoh_inactive")
pm(f"set sphere_color, {custom_color['inactive']}, %hoh_inactive")

# Color specific region to inactive color...
pm(f"set ribbon_color, {custom_color['inactive']}, %cluster2 and resi {'+'.join(color_clusters)}")
pm(f"set cartoon_color, {custom_color['inactive']}, %cluster2 and resi {'+'.join(color_clusters)}")
pm(f"set stick_color, {custom_color['inactive']}, %ret_inactive and resn ret")


# Customization

# Set view...
pm("set_view (\\")
pm("     0.719689012,   -0.683778822,    0.120294474,\\")
pm("    -0.315132022,   -0.167348713,    0.934176385,\\")
pm("    -0.618639231,   -0.710220516,   -0.335924447,\\")
pm("    -0.000630774,    0.000504352, -155.440078735,\\")
pm("    56.917179108,   13.737834930,    0.117419243,\\")
pm("   113.265342712,  197.978042603,  -20.000000000 )")

# Resize water sphere scale...
pm(f"set sphere_scale, 0.25, %hoh_active or %hoh_inactive")

# Hide the non-rhodopsin region...
pm(f"hide cartoon, (not resi {nterm}-{cterm})")
pm(f"hide ribbon, (not resi {nterm}-{cterm})")
pm(f"hide ribbon, (not resi {disp_range[0]}-{disp_range[1]})")

transp = 0
pm("bg white")
pm("set ribbon_color, gray, %cluster_gray")
pm(f"set ribbon_transparency, {transp}")
pm(f"set stick_transparency, {transp}")

# Highlight average structures...
pm("load active.pdb")
pm(f"set cartoon_transparency, {transp}, active")
pm(f"set cartoon_color, {custom_color['active']}, active")
pm(f"hide cartoon, (not resi {disp_range[0]}-{disp_range[1]}) and active")

pm("load inactive.pdb")
pm(f"set cartoon_transparency, {transp}, inactive")
pm(f"set cartoon_color, {custom_color['inactive']}, inactive")
pm(f"hide cartoon, (not resi {disp_range[0]}-{disp_range[1]}) and inactive")

pm("load average.pdb")
pm(f"set cartoon_transparency, {transp}, average")
pm(f"set cartoon_color, {custom_color['average']}, average")
pm(f"hide cartoon, (not resi {disp_range[0]}-{disp_range[1]}) and average")

# Select the transmembrane...
for k, v in TMs.items():
    pm(f"select {k}, resi {v[0]}-{v[1]} and (%average or %active or %inactive)")
    pm(f"disable {k}")

# Set lighting to rubber...
pm("set ambient, 0.05")
pm("set direct, 0.2")
pm("set spec_direct, 0")
pm("set shininess, 10.")
pm("set reflect, 0.5")
pm("set spec_count, -1")
pm("set spec_reflect, -1.")
pm("set specular, 1")
pm("set specular_intensity, 0.5")

input("Press Enter to exit...")

# Minimal, robust ab initio MD in ASH using ORCA (PBE/def2-SVP)
# Steps:
#  1) Build Fragment from XYZ (validates XYZ format)
#  2) Singlepoint to verify ORCA call
#  3) Short NVT MD via MolecularDynamics (OpenMM)

import os
from ash import Fragment, ORCATheory, Singlepoint, MolecularDynamics, OpenMM_MD_plumed
from openmm import CustomBondForce, CustomCVForce, unit
from openmm.app.metadynamics import BiasVariable

# --- user settings ---
xyz = "test-3.xyz"                      # your file
orcadir = "XXX"    # ORCA 6.1.0 dir
charge = 0
mult   = 1
# ---------------------

# --- multi-walker sync dir (shared filesystem path) ---
biasdir = "../hills"

# 1) Read XYZ (ASH expects XMol: N-atoms on line 1, comment on line 2)
frag = Fragment(xyzfile=xyz, charge=charge, mult=mult )
print(f"Loaded fragment: {frag.numatoms} atoms; charge={frag.charge}; mult={frag.mult}")

# 2) Define ORCA theory (no job-type keywords here; ASH drives the jobs)
input="!RI B3LYP 6-31G"
blocks="""
%scf
maxiter 250
end
"""

orca = ORCATheory(orcasimpleinput=input, orcablocks=blocks, numcores=8)

with open("plumed.dat","r") as f:
    plumed_str = f.read()  # feed whole PLUMED script to ASH

OpenMM_MD_plumed(
    fragment=frag, theory=orca, platform="CPU",
    timestep=0.001, simulation_time=1, temperature=300,
    integrator="LangevinMiddleIntegrator", coupling_frequency=1,
    trajectory_file_option="DCD", trajfilename="traj", traj_frequency=10,
    datafilename="mdlog",
    plumed_input_string=plumed_str  # <- key bit
)
# last-step coords are now in `frag`
frag.write_xyzfile("restart.xyz")
# (optional, good for OpenMM restarts)
frag.write_pdbfile_openmm(filename="restart.pdb", skip_connectivity=True)

print("AIMD run finished successfully.")



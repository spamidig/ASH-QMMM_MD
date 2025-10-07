#!/bin/bash
#SBATCH --nodes=1                 # Number of nodes
#SBATCH --ntasks=8                # Total number of MPI tasks
#SBATCH -A bio250125
#SBATCH -p standard
##SBATCH --qos=part-standard 
#SBATCH --time=4-00:00:00         # Walltime (hh:mm:ss)
#SBATCH -J BDG2-test-4     # Job name
#SBATCH -o myjob.o%j              # Stdout file
#SBATCH -e myjob.e%j              # Stderr file
#SBATCH --mail-user=bgeronimo3@gatech.edu
#SBATCH --mail-type=ALL           # Email when job starts/ends/fails

# OPTIONAL: Adjust to match ANVIL's recommended modules
module --force purge

# Load any MPI needed by your system that is compatible with the AmberTools conda build
module load gcc/14.2.0
module load intel/19.1.3.304

export MPI_HOME=/home/x-bdigeronimoq/openmpi-4.1.8
export PATH="$MPI_HOME/bin:$PATH"
export LD_LIBRARY_PATH="$MPI_HOME/lib:$LD_LIBRARY_PATH"
export OMPI_MCA_btl="^openib"


### Orca
export PATH=/home/x-bdigeronimoq/orca_6_1_0${PATH:+:${PATH}}
export LD_LIBRARY_PATH=/home/x-bdigeronimoq/orca_6_1_0${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
export ORCA_DIR=/home/x-bdigeronimoq/orca_6_1_0
export PATH=$PATH:$ORCA_DIR

# --- env: use your venv, keep it isolated from system site-packages ---
#source /anvil/projects/x-bio250125/ash/.venv/bin/activate
#unset PYTHONPATH
#export PYTHONNOUSERSITE=1
module load conda
source activate /anvil/projects/x-bio250125/ash/conda/ash-plumed
python test.py


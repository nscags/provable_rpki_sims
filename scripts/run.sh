#!/bin/bash
#SBATCH -J rov                                         # Name of program
#SBATCH -o log.out                                 # Name of output file
# #SBATCH -p lo-core                                # Partition (general, lo-core)
# #SBATCH --time=72:00:00                           # Timeout after 72 hours (lo-core), 12 hours (general)
#SBATCH -n 1                                       # Asking for cores
#SBATCH --mail-type=ALL                             # Event(s) that triggers email notification (BEGIN,END,FAIL,ALL)
#SBATCH --mail-user=nicholas.scaglione@uconn.edu    # Destination email address
#SBATCH --mem=32G                                   # Request RAM
# #SBATCH --mem-per-cpu=16G                         # Request RAM per cpu core, had OOM errors

# Source Virtual Environment
source ~/rpki/venv/bin/activate

# Set Job Completion Index
export JOB_COMPLETION_INDEX=$SLURM_ARRAY_TASK_ID
export PYTHONHASHSEED=$JOB_COMPLETION_INDEX
# PYTHONHASHSEED=$SLURM_TASK_ID

# Run the simulation
python3 ~/rpki/provable_rpki_sims/scripts/rov_path_sims.py
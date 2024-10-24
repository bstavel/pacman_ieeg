#!/bin/bash
# Job name:
#SBATCH --job-name=pacman_conectivity
#
# Account:
#SBATCH --account=fc_knightlab
#
# Partition:
#SBATCH --partition=savio2_bigmem
#
# Request one node:
#SBATCH --nodes=1
#
# Specify number of tasks for use case (example):
#SBATCH --ntasks-per-node=24
#
# Processors per task:
#SBATCH --cpus-per-task=1
#
# Wall clock limit:
#SBATCH --time=01:30:00
#
# SLURM Output File
#SBATCH --output=pacman_connect_job_%j.out
#SBATCH --error=pacman_connect_job_%j.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=bstavel@berkeley.edu
## Command(s) to run :

module load python
source activate ieeg_analysis2
cd /global/scratch/users/bstavel/pacman/
python scripts/pacman_connectivity.py
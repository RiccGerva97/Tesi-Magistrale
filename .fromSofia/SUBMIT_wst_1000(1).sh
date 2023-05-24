#!/bin/bash

#SBATCH -p squire #partition (queue)
#SBATCH -N 1 #number of nodes
#SBATCH -n 1 #number of cores
##SBATCH -w node1
##SBATCH --exclusive
#SBATCH --mem-per-cpu=MEMSIZE #memory pool ##Mb of RAM
##SBATCH --mem=MEMSIZE
#SBATCH -t 30-20:00 # time limit (D-HH:MM)
#SBATCH --job-name wst_patchy #job name
#SBATCH --output=log/patchy_%A_%a.o #path file to store output
#SBATCH --error=log/patchy_%A_%a.e #path file to store error messages
#SBATCH --array=1-1000

##SBATCH -o log/%x_%j.o #path file to store output
##SBATCH -e log/%x_%j.e #path file to store error messages

# mail alert at start, end and abortion of execution
##SBATCH --mail-type=ALL
# send mail to this address
##SBATCH --mail-user=sofia.chiarenza@studenti.unimi.it

##export OMP_NUM_THREADS=12

# Print the task id.
echo "SLURM_ARRAY_TASK_ID: " $SLURM_ARRAY_TASK_ID

# Name of the files
xFILE="wst_tot_1000.py"

# Job submission
cd $SLURM_SUBMIT_DIR
python $xFILE $SLURM_ARRAY_TASK_ID

exit 0


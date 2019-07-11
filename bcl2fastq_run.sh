#!/usr/bin/bash

#SBATCH -J bcl2fastq_ISSUE_20515
#SBATCH -o  bcl2fastq_ISSUE_20515%j.out
#SBATCH -e bcl2fastq_ISSUE_20515%j.err
#SBATCH -p vdb1
#SBATCH -c 32
#SBATCH -t 1-00:00:00
#SBATCH --mem-per-cpu=8G
#SBATCH --mail-type=ALL
#SBATCH --mail-user=AMAILBOX

module purge
module load bcl2fastq2-v2.20.0

bcl2fastq --runfolder-dir RUNPATH \
          --output-dir OUTDIR \
          --sample-sheet ss \
          --barcode-mismatches 0 \
          --no-bgzf-compression \
          --create-fastq-for-index-reads
          

## note -r and -w should equal the number of samples in the sample sheet
## -p can be the rest of the node
## bcl2fastq does not seem to be able to pull resources from multiple nodes, so don't set -p to greater than 36
#Forprocessing,ifyourcomputingplatformsupportsthreading,thesoftwaremanagesthethreadsbythefollowingdefaults:}4threadsforreadingthedata}4threadsforwritingthedata}20%fordemultiplexingdata}100%forprocessingdemultiplexeddat 

          # -r 4 -w 4 -p 14 \

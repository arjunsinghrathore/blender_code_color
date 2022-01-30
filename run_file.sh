#!/bin/bash
#SBATCH --time=48:00:00
##SBATCH -p gpu --gres=gpu:1
#SBATCH -n 1
#SBATCH -N 1 
#SBATCH --mem=10GB
#SBATCH -J render_MI_val
##SBATCH -C p100
##SBATCH --constraint=v100
#SBATCH -o /users/aarjun1/data/aarjun1/blender_render-color_pos/logs/MI_%A_%a_%J.out
#SBATCH -e /users/aarjun1/data/aarjun1/blender_render-color_pos/logs/MI_%A_%a_%J.err
#SBATCH --account=carney-tserre-condo
##SBATCH --array=0-1


##SBATCH -p gpu

cd ~/data/aarjun1/blender_render-color_pos/

module load anaconda/3-5.2.0
module load python/3.5.2
# module load opencv-python/4.1.0.25
# module load cuda
module load cudnn/7.4
module load cuda/10.0.130

source activate color_CNN


echo $SLURM_ARRAY_TASK_ID

# python -u file_management.py #--job_number $SLURM_JOB_ID --gpu_index $CUDA_VISIBLE_DEVICES #-n 1 -v single_illuminant -j $SLURM_ARRAY_TASK_ID

python -u file_management2.py #--job_number $SLURM_JOB_ID --gpu_index $CUDA_VISIBLE_DEVICES #-n 1 -v single_illuminant -j $SLURM_ARRAY_TASK_ID



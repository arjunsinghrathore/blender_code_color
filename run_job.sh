#!/bin/bash
#SBATCH --time=260:00:00
#SBATCH -p gpu --gres=gpu:5
#SBATCH -n 1
#SBATCH -N 1 
#SBATCH --mem=40GB
#SBATCH -J render_MI_val
##SBATCH -C quadrortx
##SBATCH --constraint=v100
#SBATCH -o /users/aarjun1/data/aarjun1/blender_render-color_pos/logs/MI_%A_%a_%J.out
#SBATCH -e /users/aarjun1/data/aarjun1/blender_render-color_pos/logs/MI_%A_%a_%J.err
#SBATCH --account=carney-tserre-condo
##SBATCH --array=0-25


##SBATCH -p gpu

cd ~/data/aarjun1/blender_render-color_pos/

module load python/3.5.2
module load blender/2.79
# module load cuda
module load cudnn/7.4
module load cuda/10.0.130
module load openexr/2.2.1

module load opencv-python
# module load anaconda/3-5.2.0

source ~/ENV/bin/activate


# python generate_dataset.py -n 10 -v ben_ccv_lambert_1 -j $SLURM_ARRAY_TASK_ID

# python generate_dataset.py -n 10 -v texture_CC

echo $SLURM_ARRAY_TASK_ID

python -u generate_dataset.py --job_number $SLURM_JOB_ID --gpu_index $CUDA_VISIBLE_DEVICES #-n 1 -v single_illuminant -j $SLURM_ARRAY_TASK_ID

# python generate_dataset.py -n 1000 -v multi_illuminant -j $SLURM_ARRAY_TASK_ID

# python generate_dataset.py -n 1000 -v multi_illuminant_val -j $SLURM_ARRAY_TASK_ID



# problems:
# find validation textures ? split original texture set into train/val

# create new blobs for validation ?



#######################  single illuminant - multi illuminant single object no background

# 1- generate training sets with current textures
 
# 2- generate validation sets with different textures

# 3- prepare training script

#!/usr/bin/env bash
# CCV rendering script: Queues rendering processes onto ccv
# {{NAME}} fields will be replaced by parameters

#SBATCH --gres=gpu:{{n_gpus}}
#SBATCH -t{{time_in_hours}}:00:00
#SBATCH -J rendering
#SBATCH -p {{queue}}
#SBATCH -o {{output_fname}}
#SBATCH -e {{error_fname}}
## COMMENTED OUT: SBATCH -N {{n_nodes}}
## COMMENTED OUT: SBATCH --mem={{n_mb_of_mem}}

render_offset=$1
start=`date +%s`

# Setup environment
module load python/2.7.12 # boost/1.49.0
module load cuda/9.1.85.1 #nvidia-driver/340.65 cudnn/6.0 openblas/0.2.19
module load libpng12/1.2.57 hdf5/1.10.0
module load opencv/3.2.0 blender/2.79 openexr/2.2.1 #opengl/nvidia-375.20

cd $(dirname {{generation_script}})
#NOTE: USER MUST INSTALL REQUIREMENTS FOR THEIR CCV USER

if [ ! -d ../data ]
then
    mkdir ../data
fi

job_index=$(( render_offset + SLURM_ARRAY_TASK_ID ))

render_index=$(( job_index * {{batch_size}} ))

echo Command: {{generation_script}} -v {{version}} -g all -n {{batch_size}} -i $render_index
{{generation_script}} -v {{version}} -g all -n {{batch_size}} -i $render_index

end=`date +%s`
runtime=$((end-start))
echo "$runtime"
~:echo == DONE IN "$runtime" SECONDS ==
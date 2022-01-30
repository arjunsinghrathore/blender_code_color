#!/usr/bin/env python
import stat
import argparse
import time
import subprocess as sb
from rsync_ccv import rsync_to_ccv
import sys, os

# TODO warning -- stty: standard input: Inappropriate ioctl for device
# TODO still trying to connect to DB all time?

sys.path.append(os.path.abspath('..'))
from config import source_path, ccv_source_path, ccv_resources_path, ccv_host_address, resources_path, ccv_log_path, \
    db_host, db_port, db_username
from rendering_parameters import initialize_parameters

# Maximum size of a job array on CCV. Split into multiple arrays if exceeded.
max_job_array_size = 512


# send source code to ccv
def rsync_source_code():
    rsync_to_ccv(source_path, ccv_source_path, exclusions=['.git', 'images_*', 'data', 'dan', '*.npy', '*.pyc'])


# send models and other blender data to ccv
def rsync_3d_models():
    rsync_to_ccv(resources_path, ccv_resources_path,
                 exclusions=['.git', 'david', 'deprecated', 'random_objects', 'random_surfs', 'facegen',
                             'hdr_doesntwork', 'models_more_zipped', 'nice_textures (copy)', 'novel_objects_3ds',
                             'random_mballs', 'rithesh', 'scrap', 'script', 'tarun_heightmaps', '*.blend1', '*.zip',
                             'shapenet/ShapeNetCore.v2.subset'])


# ------------------------------------------------------------------------------#
def template_to_script(template_filename, output_filename, parameters):
    # Load template script, replace items in dictionary and write to output
    data = open(template_filename, 'rt').read()
    # Fill in parameters
    for k, v in parameters.iteritems():
        data = data.replace('{{%s}}' % k, str(v))
    # Write to executable file
    try:
        os.remove(output_filename)
    except OSError:
        pass
    umask_original = os.umask(0)
    try:
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
        mode = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH | stat.S_IRGRP | stat.S_IROTH
        fd = os.open(output_filename, flags, mode)
        with os.fdopen(fd, 'w') as fid:
            fid.write(data)
    finally:
        os.umask(umask_original)


def create_all_scripts(version=0, batch_size=50, total_render_count=0):
    # Creates the SLURM render script
    # full_db_host = '{0}@{1}'.format(db_username, db_host)
    curr_time = time.time()
    parameters = dict(
        n_nodes=1,
        n_cpu_cores=1,
        n_gpus=1,
        # TODO make hours an input option? or go back to 2hr
        time_in_hours=2,
        # n_mb_of_mem=10 * 1024,
        queue='gpu',
        batch_size=batch_size,
        version=version,
        total_render_count=total_render_count,
        output_fname=os.path.join(ccv_log_path, 'rendering_output_{0}.txt'.format(curr_time)),
        error_fname=os.path.join(ccv_log_path, 'rendering_error_{0}.txt'.format(curr_time)),
        generation_script=os.path.join(ccv_source_path, 'generate_dataset.py'),
        # db_host=full_db_host,
        # db_port=db_port
    )

    slurm_filename = os.path.join(source_path, 'tmp_slurm.{0}.{1}.sh'.format(parameters['queue'], curr_time))
    slurm_template_filename = os.path.join(source_path, 'ccv/ccv_render_template.sh')

    template_to_script(slurm_template_filename, slurm_filename, parameters)
    return slurm_filename


# ------------------------------------------------------------------------------#
def run_on_ccv(slurm_filename, job_0=0, n_jobs=1):
    # Split up larger job arrays
    if n_jobs > max_job_array_size:
        for i, j0 in enumerate(xrange(job_0, job_0 + n_jobs, max_job_array_size)):
            nj = min(max_job_array_size, job_0 + n_jobs - j0)
            print '*** JOB SLICE %d: [%d - %d[' % (i, j0, j0 + nj)
            run_on_ccv(slurm_filename, job_0=j0, n_jobs=nj)
    else:
        slurm_filename = os.path.join(ccv_source_path, os.path.basename(slurm_filename))
        sbatch_command = [
            "ssh {0} 'ssh login003 'sbatch --array=0-{1} {2} {3}' ' ".format(  # TODO likely can remove inner ssh
                ccv_host_address,
                n_jobs - 1,
                slurm_filename,
                job_0)]
        print "-" * 80
        print "Sbatch command: "
        print sbatch_command
        print "-" * 80

        aa = sb.Popen(sbatch_command, shell=True, stdout=sb.PIPE, stderr=sb.PIPE)
        out, err = aa.communicate()

        if not err:
            print "command:  worked"
        else:
            print "error: ", err


# ------------------------------------------------------------------------------#
def main():
    parser = argparse.ArgumentParser(description="""""")
    parser.add_argument('--n_jobs', '-n', default=50, type=int,
                        help="""n_jobs""")
    parser.add_argument('--version', '-v', default=None, type=str,
                        help="""version""")
    # parser.add_argument('--n_iterations', '-i', default=5, type=int,
    #                     help="""number of batches per job""")
    parser.add_argument('--batch_size', '-b', default=50, type=int,
                        help="""number of renders per batch""")
    # parser.add_argument('--n_gpus', '-g', default=2, type=int,
    #                     help="""number of GPUs to render on""")
    parser.add_argument('--skip_model_sync', '-s', default=False, action='store_true',
                        help="""skip rsync-ing the models directory""")
    args = parser.parse_args()
    n_jobs = args.n_jobs
    version = args.version
    # n_iterations = args.n_iterations
    batch_size = args.batch_size
    # n_gpus = args.n_gpus

    # For gridded renders, find the number of renders required to fill grid
    p = initialize_parameters(version, batch_size)
    num_renders = p.get('num_gridded_parameters', 0)
    # if num_renders:
    #     renders_per_job = (n_iterations * batch_size * n_gpus)
    #     n_jobs = (num_renders - 1) // renders_per_job + 1  # number of jobs rounded up
    #     print 'Running %d jobs with %d iterations, %d gpus, and batch size %d for gridded render [total=%d].' % (
    #         n_jobs, n_iterations, n_gpus, batch_size, num_renders)
    if num_renders:
        n_jobs = (num_renders - 1) // batch_size + 1  # number of jobs rounded up
        print 'Running %d jobs with batch size %d for gridded render [total=%d].' % (
            n_jobs, batch_size, num_renders)
    slurm_filename = create_all_scripts(version=version, batch_size=batch_size, total_render_count=num_renders)
    rsync_source_code()
    if not args.skip_model_sync:
        rsync_3d_models()

    run_on_ccv(slurm_filename, n_jobs=n_jobs)


# ------------------------------------------------------------------------------#
if __name__ == "__main__":
    main()

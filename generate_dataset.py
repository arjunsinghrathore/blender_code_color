#!/usr/bin/env python

import argparse
import os
import config
from blender_manager import RenderManager
from rendering_parameters import initialize_parameters, setup_output_directory
from utils.logging import announce
from utils.render_passes import get_passes_from_exr, add_png_pass, add_slant_tilt_pass, add_contour_z_pass, \
    h5_from_passes, add_color_ground_truth_pass, add_xyz_dkl_pass, png_from_each_pass, pickle_render, \
    black_background_mod, invert_mod
import sys
# from utils.render_db import RenderDB


# TODO sel model by class
# TODO adding timing

def generate_dataset(gpu_index, version, debug_passes, grid_index, batch_size, db=None, force_continue=None, job_number=None):
    """
    Initialize user specified rendering parameters,
    iterate through generated render conditions and
    save render data in specified formats
    """
    parameters = initialize_parameters(version=version, grid_index=grid_index,
                                       batch_size=batch_size, gpu_index=gpu_index, force_continue=force_continue, job_number=job_number)
    setup_output_directory(parameters)
    with RenderManager(parameters) as render_manager:
        for render in render_manager:
            try:
                if render is not None:  # can be None if force_continue is True
                    announce('Render {0} complete'.format(render['index']))
                    if render['needs_pass_work']:
                        passes = get_passes(render)
                        save_files(passes, render, debug_passes)
                    announce('Data from render {0} saved'.format(render['index']))
                    if config.MONGO and db:
                        render_grid = render.get('grid')
                        if render_grid:  # mongo can't use lists as keys
                            db_grid = {}
                            for keys, value in render_grid.iteritems():
                                key_string = ' '.join(str(key) for key in keys)
                                db_grid[key_string] = value
                            render['grid'] = db_grid
                        db.save_entry(render, render['output_filename'] + '.h5')
                        render['grid'] = render_grid  # reset grid param to tuple or None
            except:
                raise
        
        render_manager.save_dataset()


def get_passes(render):
    """
    Retrieve the render data saved into png and exr files by blender
    Note that the PNG has the 'photo-realistic' color image, EXR has all other ground truth data
    """
    output_parameters = render['output']
    base_file = render['output_file']
    passes_list = output_parameters['passes']
    stereo = output_parameters['stereo']
    exr_file = base_file + '.exr'
    passes = get_passes_from_exr(exr_file, passes_list)
    # TODO frame file/save files after naming convention fix for anim
    if 'color' in passes_list:
        if stereo:
            l_png_file = base_file + '_L.png'
            r_png_file = base_file + '_R.png'
            add_png_pass(passes, l_png_file, '_L')
            add_png_pass(passes, r_png_file, '_R')
        else:
            png_file = base_file + '.png'
            add_png_pass(passes, png_file)
    if 'slant' in passes_list or 'tilt' in passes_list:
        add_slant_tilt_pass(passes, passes_list, render['camera']['rotation'])
    if 'contour' in passes_list or 'shallow_z' in passes_list:
        add_contour_z_pass(passes, passes_list)
    if 'disparity' in passes_list:
        pass
        # TODO add_disparity_pass()
    if 'color_ground_truth' in passes_list:
        add_color_ground_truth_pass(passes, passes_list)
    if 'combined_xyz' in passes_list or 'combined_dkl' in passes_list:
        add_xyz_dkl_pass(passes, passes_list)
    for p in passes_list:
        if p.endswith('_black'):
            black_background_mod(p, passes)
        if p.endswith('_inv'):
            invert_mod(p, passes)
    return passes


def save_files(passes, render, debug_passes):
    """
    Save render data into specified file types, remove unwanted file types
    """
    output_parameters = render['output']
    png_passes = output_parameters.get('png_passes')
    file_types = output_parameters['file_types']
    stereo = output_parameters['stereo']
    base_file = render['output_file']
    animate = render.get('animate')
    if animate:
        frames = animate['frames']
        for i_frame in range(frames):
            frame_file = base_file.replace('####', '%04d' % i_frame)
            save_and_delete_files(render, frame_file, file_types, passes, stereo, debug_passes)
    else:
        save_and_delete_files(render, base_file, file_types, passes, stereo, debug_passes, png_passes)


def save_and_delete_files(render, base_file, file_types, passes, stereo, debug_passes, png_passes=None):
    exr_file = base_file + '.exr'
    if 'pkl' in file_types:  # note: just saves parameter dictionary
        pickle_render(base_file, render)
    if 'h5' in file_types:
        h5_from_passes(base_file, passes)
    if debug_passes or png_passes:
        png_from_each_pass(base_file, passes, png_passes)
    if 'exr' not in file_types and os.path.exists(exr_file):
        os.remove(exr_file)
    if 'png' not in file_types:
        l_png_file = base_file + '_L.png'
        r_png_file = base_file + '_R.png'
        png_file = base_file + '.png'
        if stereo and os.path.exists(l_png_file) and os.path.exists(r_png_file):
            os.remove(l_png_file)
            os.remove(r_png_file)
        elif os.path.exists(png_file):
            os.remove(png_file)


def main():
    # import sys
    # sys.argv=['']
    # del sys
    """
    Parse command line arguments
    Call main generating function
    """
    def str2bool(v):
        if v.lower() in ('yes', 'true', 't', 'y', '1'):
            return True
        elif v.lower() in ('no', 'false', 'f', 'n', '0'):
            return False
        else:
            raise argparse.ArgumentTypeError('Boolean value expected.')

    # try:
    parser = argparse.ArgumentParser(description='hello')
    parser.add_argument('--gpu_index', type=str,
                        default=None, help="""gpu index to use""")
    parser.add_argument('--version', type=str,
                        default='single_illuminant', help="""VERSION string""")
    parser.add_argument('--verbose', action='store_true',
                        default=True, help="""verbose""")
    parser.add_argument('--use_db', type=str2bool, nargs='?',
                        const=False, default=config.MONGO, help="""use mongodb to store entries""")
    parser.add_argument('--debug_passes', action="store_true",
                        default=False, help="""save all passes as images.""")
    parser.add_argument('--grid_index', type=int,
                        default=0, help="""render index of batch (for grid parameters)""")
    parser.add_argument('--batch_size', type=int,
                        default=150000, help="""render batch of n images""")
    parser.add_argument('--force_continue', action='store_true',
                        default=None, help="""don't raise exceptions, keep trying next render""")
    parser.add_argument('--job_number', type=int,
                        default=None, help="""job number for batch render on ccv""")

    args = parser.parse_args()

    gpu_index = args.gpu_index
    version = args.version
    debug_passes = args.debug_passes
    config.VERBOSE = args.verbose
    config.MONGO = args.use_db
    grid_index = args.grid_index
    batch_size = args.batch_size
    force_continue = args.force_continue
    job_number = args.job_number

    # job_number = sys.argv[1]

    announce('This is version: {0}'.format(version), '#')
    announce('This is jobID: {0}'.format(job_number), '#')
    announce('This is batch_size: {0}'.format(batch_size), '#')
    announce('This is gpu_index: {0}'.format(gpu_index), '#')
    if config.MONGO:
        with RenderDB() as db:
            generate_dataset(gpu_index=gpu_index,
                             version=version,
                             debug_passes=debug_passes,
                             grid_index=grid_index,
                             batch_size=batch_size,
                             db=db,
                             force_continue=force_continue)
    else:
        generate_dataset(gpu_index=gpu_index,
                         version=version,
                         debug_passes=debug_passes,
                         grid_index=grid_index,
                         batch_size=batch_size,
                         force_continue=force_continue,
			 job_number=job_number)


if __name__ == "__main__":
    main()

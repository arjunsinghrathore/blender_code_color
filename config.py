#!/usr/bin/env python
import os
import getpass as gp

# rendering on cluster
user_name = gp.getuser()
node_name = os.uname()[1]

VERBOSE = True
MONGO = False
source_path = os.path.dirname(os.path.realpath(__file__))
# db_username = 'aarjun1'  # Use current user
# # db_keyfile = '/home/{0}/.ssh/id_rsa'.format(user_name)
# db_keyfile = '/home/aarjun1/.ssh/id_rsa'
# db_use_tunnel = True
# db_port = 27017
# db_host = 'g15.clps.brown.edu'
# db_ip = '127.0.0.1'
# db_name = 'darpa'
# db_collection = 'kitchen'
# TODO clean branch
# TODO think about eliminating config
# TODO refactor out into USER section for config, dataset versions
# if node_name in ['g10', 'g12', 'g13', 'g14', 'g17', 'x6', 'x7', 'x8']:  # Phil
#     resources_path = '/media/data_cifs/darpa/kitchen/3d_models'
#     output_path = '/media/data_cifs/darpa/laxtest'
#     ccv_home = '/gpfs/data/tserre/data/darpa'
#     ccv_source_path = os.path.join(ccv_home, 'src')
#     ccv_resources_path = os.path.join(ccv_home, '3d_models')
#     ccv_log_path = os.path.join(ccv_home, 'logs')
#     ccv_host_address = 'pbayer@ssh.ccv.brown.edu'
#     ccv_transfer_address = 'pbayer@transfer.ccv.brown.edu'

if node_name.startswith('gpu') or node_name.startswith('node') or node_name.startswith('login'):  # CCV
    # base_path = '/gpfs/data/tserre/data/darpa'
    # resources_path = os.path.join(base_path, '3d_models')

    # resources_path = '/gpfs/scratch/azerroug/blender_ressources'
    # base_out = '/gpfs/scratch/azerroug/blender_render'
    resources_path = '/gpfs/scratch/aarjun1/train_data'
    base_out = '/gpfs/scratch/aarjun1/blender_data'
    output_path =  os.path.join(base_out, 'data_no_filmic')
    # db_keyfile = '/users/aarjun1/.ssh/id_rsa'
    # db_use_tunnel = False  # Tunnel is done by master bash script
else:
    resources_path = "./Assets"
    output_path = "./Images"


import os

import argparse
import pickle

# rename all files
# make train dir
# move them to traindir 
# (same for val)
# save names in list

# read all pickles and save in one pickle with name list
# save pickles in
# for both train and val


# read all file names

# read all pickle files

def organize_set(args):
    n_images = 1000
    train_dir = args.train_folder
    val_dir = args.val_folder
    out_dir = args.output_folder

    new_train_dir = os.path.join(out_dir, 'train')
    new_train_dir_images = os.path.join(new_train_dir, 'images')
    new_train_dir_gt_i = os.path.join(new_train_dir, 'gt_i')
    new_train_dir_gt_r = os.path.join(new_train_dir, 'gt_r')
    
    os.makedirs(new_train_dir, exist_ok=True)
    os.makedirs(new_train_dir_images, exist_ok=True)
    os.makedirs(new_train_dir_gt_i, exist_ok=True)
    os.makedirs(new_train_dir_gt_r, exist_ok=True)
    
    train_subdirs = os.listdir(train_dir)
    
    name_list = []
    illuminants = []
    for i in range(len(train_subdirs)):
        
        for j in range(n_images):
            name_1 = os.path.join(train_dir, str(i), "%04d.png"%j) 
            name_1_gti = os.path.join(train_dir, str(i), "%04d.gt_i.png"%j) 
            name_1_gtr = os.path.join(train_dir, str(i), "%04d.gt_r.png"%j) 
            
            name_2 = os.path.join(new_train_dir_images, "%02d_%04d.png"%(i,j))
            name_2_gti = os.path.join(new_train_dir_gt_i, "%02d_%04d.png"%(i,j))
            name_2_gtr = os.path.join(new_train_dir_gt_r, "%02d_%04d.png"%(i,j))

            try:
                os.rename(name_1,name_2) 
            except:
                pass
            try:
                os.rename(name_1_gti, name_2_gti) 
            except:
                pass
            try:
                os.rename(name_1_gtr, name_2_gtr) 
            except:
                pass
             
            name_list.append("%02d_%04d.png"%(i,j))
        
        with open(os.path.join(train_dir, "%d/%d.pickle"%(i,i)) , 'rb') as f:
            illuminants += pickle.load(f)
    
    with open(os.path.join(new_train_dir, 'data.pickle'), 'wb') as f:
        pickle.dump([name_list, illuminants], f)
    
    # new_val_dir = os.path.join(out_dir, 'val')    
    # new_val_dir_images = os.path.join(new_val_dir, 'images')
    # new_val_dir_gt_i = os.path.join(new_val_dir, 'gt_i')
    # new_val_dir_gt_r = os.path.join(new_val_dir, 'gt_r')

    # os.makedirs(new_val_dir, exist_ok=True)
    # os.makedirs(new_val_dir_images, exist_ok=True)
    # os.makedirs(new_val_dir_gt_i, exist_ok=True)
    # os.makedirs(new_val_dir_gt_r, exist_ok=True)

    # val_subdirs = os.listdir(val_dir)

    # name_list = []
    # illuminants = []
    # for i in range(len(val_subdirs)):
        
    #     for j in range(n_images):
    #         name_1 = os.path.join(val_dir, str(i), "%04d.png"%j) 
    #         name_1_gti = os.path.join(val_dir, str(i), "%04d.gt_i.png"%j) 
    #         name_1_gtr = os.path.join(val_dir, str(i), "%04d.gt_r.png"%j) 
            
    #         name_2 = os.path.join(new_val_dir_images, "%02d_%04d.png"%(i,j))
    #         name_2_gti = os.path.join(new_val_dir_gt_i, "%02d_%04d.png"%(i,j))
    #         name_2_gtr = os.path.join(new_val_dir_gt_r, "%02d_%04d.png"%(i,j))

    #         try:
    #             os.rename(name_1,name_2) 
    #         except:
    #             pass
    #         try:
    #             os.rename(name_1_gti, name_2_gti) 
    #         except:
    #             pass
    #         try:
    #             os.rename(name_1_gtr, name_2_gtr) 
    #         except:
    #             pass

    #         name_list.append("%02d_%04d.png"%(i,j))
        
    #     with open(os.path.join(train_dir, "%d/%d.pickle"%(i,i)) , 'rb') as f:
    #         illuminants += pickle.load(f)

    # with open(os.path.join(new_val_dir, 'data.pickle'), 'wb') as f:
    #     pickle.dump([name_list, illuminants], f)


def main():

    parser = argparse.ArgumentParser(description="""organize dataset""")
    
    parser.add_argument('--train-folder', type=str,
                        default=None, help="""training data folder""")
    parser.add_argument('--val-folder', type=str,
                        default=None, help="""validation data folder""")
    parser.add_argument('--output-folder', type=str,
                        default=None, help="""output folder for the dataset""")

    # parser.add_argument('--version', '-v', type=str,
    #                     default=None, help="""VERSION string""")
    # parser.add_argument('--verbose', '-V', action='store_true',
    #                     default=False, help="""verbose""")
    # parser.add_argument('--use_db', '-d', type=str2bool, nargs='?',
    #                     const=True, default=config.MONGO, help="""use mongodb to store entries""")
    # parser.add_argument('--debug_passes', '-p', action="store_true",
    #                     default=False, help="""save all passes as images.""")
    # parser.add_argument('--grid_index', '-i', type=int,
    #                     default=0, help="""render index of batch (for grid parameters)""")
    # parser.add_argument('--batch_size', '-n', type=int,
    #                     default=None, help="""render batch of n images""")
    # parser.add_argument('--force_continue', '-f', action='store_true',
    #                     default=None, help="""don't raise exceptions, keep trying next render""")
    # parser.add_argument('--job_number', '-j', type=int,
    #                     default=None, help="""job number for batch render on ccv""")

    # dataset folder
    # output folder
    
    args = parser.parse_args()

    organize_set(args)



if __name__ == "__main__":
    main()

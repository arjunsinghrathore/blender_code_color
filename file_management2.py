import os
import shutil
from tqdm import tqdm
import numpy as np
import cv2
import pickle

def file_io():

  files_list = os.listdir('/users/aarjun1/scratch/train_data/render_textures/textures_sorted')
  files_list2 = os.listdir('/users/aarjun1/scratch/train_data/textures_sorted')

  file_list3 = [filee for filee in files_list if filee not in files_list2]

  for i, fil in tqdm(enumerate(file_list3)):
    fname = '/users/aarjun1/scratch/train_data/render_textures/temp_test/' + fil
    shutil.copy('/users/aarjun1/scratch/train_data/render_textures/textures_sorted/'+fil, fname)
      



if __name__ == '__main__':
  file_io()


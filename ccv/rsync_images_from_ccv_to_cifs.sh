#!/usr/bin/env bash
# Moves files from rendering directory to Isilon storage
# To be run on transfer.ccv.brown.edu (in a screen session or tmux)

rsync -av --remove-source-files pbayer@transfer.ccv.:/users/seberhar/darpa/data/images_607 /cifs/data/tserre/seberhar/darpa/kitchen

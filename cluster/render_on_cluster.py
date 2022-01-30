#!/usr/bin/env python
import os, stat
import subprocess as sp
import argparse, os
from config import source_path, model_data_path, db_host, db_port, db_username, cluster_password_path, cluster_home, username, local_home
import time
from rendering_parameters import initialize_parameters
import numpy as np
from mesos_cook import CookClient, Job
from uuid import uuid1
import cPickle
import requests
#------------------------------------------------------------------------------#
def run_on_cluster(version, batch_size, n_gpus, n_jobs=1):
    q = raw_input("Are you sure you'd like to run these jobs? (y/n)")
    if q == "n":
        return
    else:
        if n_gpus == 0:
            schedule_all_jobs(version, batch_size, n_jobs)
        else:           
            schedule_limited_jobs(version, batch_size, n_gpus, n_jobs)
        return
#------------------------------------------------------------------------------#
def schedule_all_jobs(version, batch_size, n_jobs=1):
    if cluster_password_path:
        cluster_username, cluster_password = cPickle.load(open(cluster_password_path, "rb"))    
        cook = CookClient('http://serrep1.services.brown.edu:12321', cluster_username, cluster_password)
    else:
        print "No password file for cluster found"
        return

    jobs = []
    group_id = str(uuid1())
    for i in range(n_jobs):
        job = Job(
        name = 'batch_%d'%(i), 
        uuid = str(uuid1()), 
        group = group_id,
        priority = 10,
        command = "/bin/bash -c 'source {home}/.virtualenvs/rendering/bin/activate; \
                python {home}/src/darpa/rendering/generate_dataset.py \
                -v {version} -i {index} -g 0 -n {batch_size}'".format(home = cluster_home, version = version,
                    index = i*batch_size,batch_size = batch_size), 
        max_retries = 1, cpus = .1, mem = 128, gpus = 1)
        jobs.append(job)
    cook.launch(jobs)
    return

#------------------------------------------------------------------------------#
def schedule_limited_jobs(version, batch_size, n_gpus, n_jobs=1):
    if cluster_password_path:
        cluster_username, cluster_password = cPickle.load(open(cluster_password_path, "rb"))    
        cook = CookClient('http://serrep1.services.brown.edu:12321', cluster_username, cluster_password)
    else:
        print "No password file for cluster found"
        return

    jobs_scheduled = 0
    jobs_running = 0
    jobs = {}
    while jobs_scheduled < n_jobs:
        if jobs_running < n_gpus:
            job_uuid = str(uuid1())
            job = Job(
            name = 'batch_%d'%(jobs_scheduled), 
            uuid=job_uuid, 
            priority = 50, 
            command = "/bin/bash -c 'source {home}/.virtualenvs/rendering/bin/activate; \
                    python {home}/src/darpa/rendering/generate_dataset.py \
                    -v {version} -i {index} -g 0 -n {batch_size}'".format(home = cluster_home, version = version,
                        index = jobs_scheduled*batch_size, batch_size = batch_size), 
            max_retries = 1, cpus = .1, mem = 128, gpus = 1)
            jobs_scheduled += 1
            jobs_running += 1
            jobs[job_uuid] = job
            cook.launch(job)
        else:
            while jobs_running >= n_gpus:        
                for uuid, job in jobs.iteritems():
                    r = requests.get(cook._rawscheduler, auth=cook._auth, params={'job': [uuid]})
                    print r.json()[0][u'status']
                    if r.json()[0][u'status'] == u'completed':
                        jobs.pop(uuid, None)
                        jobs_running -= 1
                    elif r.json()[0][u'status'] == u'failed': #note this doesn't work
                        print "job failed, trying again"
                        cook.launch(jobs[uuid])
                    r = None
                time.sleep(1)
        #print "jobs scheduled/completed: {0}\njobs running: {1}\ntotal jobs: {2}\ngpus: {3}".format(jobs_scheduled,jobs_running,n_jobs,n_gpus)
    return


#------------------------------------------------------------------------------#
def main():

    parser = argparse.ArgumentParser(description="""""")
    parser.add_argument('--n_jobs', '-n', default = 500, type=int, help="""n_jobs""")
    parser.add_argument('--version', '-v', default=0, type=str, help="""version""")
    parser.add_argument('--batch_size', '-b', default=50, type=int, help="""number of renders per batch""")
    parser.add_argument('--n_gpus', '-g', default=0, type=int, help="""number of GPUs to render on, if 0 it will schedule all jobs at once""")
    args = parser.parse_args()
    n_jobs  = args.n_jobs
    version = args.version
    batch_size = args.batch_size
    n_gpus = args.n_gpus 

    # For gridded renders, find the number of renders required to fill grid
    p = initialize_parameters(version)
    num_renders = p.get('num_gridded_elements', 0)
    if num_renders:
        n_jobs = (num_renders-1) // batch_size + 1 # number of jobs roounded up
        render_type = "gridded"
    else:
        render_type = "normal"
        num_renders = batch_size*n_jobs

    #sync cluster nodes
    sp.call('{0}/src/darpa/rendering/rsync_cluster.sh {1}'.format(local_home, username),shell=True)

    gpus_info = ""
    if n_gpus > 0:
        gpus_info = str(n_gpus)
    else:
        gpus_info = "all available"

    print 'Running %d jobs with %s gpus, and batch size %d for %s render [total=%d].' % (n_jobs, gpus_info, batch_size, render_type, num_renders)
    run_on_cluster(n_jobs=n_jobs, version = version, batch_size=batch_size, n_gpus = n_gpus)

#------------------------------------------------------------------------------#
if __name__=="__main__":
    main()

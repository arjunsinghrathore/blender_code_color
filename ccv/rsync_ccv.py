#!/usr/bin/env python
import subprocess as sb
from Queue import Queue, Empty
from threading import Thread
import sys, os

sys.path.append(os.path.abspath('..'))
from config import ccv_transfer_address


def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()


def exec_and_communicate(command):
    # Run command, pipe out+err and wait to finish
    aa = sb.Popen(command, shell=True, stdout=sb.PIPE, stderr=sb.PIPE)
    q = Queue()
    t = Thread(target=enqueue_output, args=(aa.stderr, q))
    t.daemon = True
    while not aa.poll():
        stdoutdata = aa.stdout.readline()
        try:
            stderrdata = q.get_nowait()
            print "err: ", stderrdata
        except Empty:
            pass
        if stdoutdata:
            sys.stdout.write(stdoutdata)
        else:
            break


def rsync_to_ccv(src_dir, dest_dir, exclusions=None, dest_address=ccv_transfer_address):
    # Sync folder on CCV to be the same as a local folder
    assert not ' ' in src_dir
    assert not ' ' in dest_dir
    exclusions = [("""--exclude '%s'""" % e) for e in exclusions]
    dest = "%s:%s" % (dest_address, dest_dir)
    command = 'rsync -avzh --progress --delete ' + ' '.join(exclusions) + ' ' + src_dir + '/* ' + dest
    print "-" * 80
    print "RSYNC command: "
    print command
    print "-" * 80
    exec_and_communicate(command)

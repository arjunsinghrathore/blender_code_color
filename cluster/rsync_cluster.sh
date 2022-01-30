#!/bin/bash

if [ "$1" == "" ]; then
	echo "usage: rsync_cluster [ cluster user name ]"
else
	if [ "$(hostname)" != "serrep1" ] || [ "$(hostname)" != "p1" ]; then 
		rsync -az ~/.virtualenvs/rendering $1@serrep1.services.brown.edu:~/.virtualenvs
		rsync -az ~/pass*.p $1@serrep1.services.brown.edu:~/
		rsync -az ~/src/darpa $1@serrep1.services.brown.edu:~/src
		echo "serrep1 synced"
	fi

	if [ "$(hostname)" != "serrep2" ]; then
		rsync -az ~/.virtualenvs/rendering $1@serrep2.services.brown.edu:~/.virtualenvs
		rsync -az ~/pass*.p $1@serrep2.services.brown.edu:~/
		rsync -az ~/src/darpa $1@serrep2.services.brown.edu:~/src 
		echo "serrep2 synced"
	fi

	if [ "$(hostname)" != "serrep3" ]; then
		rsync -az ~/.virtualenvs/rendering $1@serrep3.services.brown.edu:~/.virtualenvs
		rsync -az ~/pass*.p $1@serrep3.services.brown.edu:~/
		rsync -az ~/src/darpa $1@serrep3.services.brown.edu:~/src
		echo "serrep3 synced"
	fi

fi
#!/bin/bash
set -x

if [ "$1" = 'master' ]
then
	echo "Run master ..."
	python main.py
	echo "Run enqueue worker ..."
	nohup python enqueue_worker.py >/tmp/webcrawler.log 2>&1 &
	echo "Run dequeue worker ..."
	nohup python dequeue_worker.py >/tmp/webcrawler.log 2>&1 &
	echo "Done !"
elif [ "$1" = 'crawler' ]
then
	NUM_WORKERS=${2:-5}
	for (( i=0; i<=$NUM_WORKERS; i++ ))
	do
		echo "Run crawler $i ..."
		nohup python crawler.py >/tmp/webcrawler.log 2>&1 &
	done
	echo "Done !"
fi

tail -F /tmp/webcrawler.log
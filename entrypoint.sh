#!/bin/bash
set -x

if [ "$1" = 'master' ]
then
	echo "Run master ..." >> /tmp/webcrawler.log
	python main.py
	echo "Run enqueue worker ..." >> /tmp/webcrawler.log
	nohup python enqueue_worker.py >/dev/null 2>&1 &
	echo "Run dequeue worker ..."
	nohup python dequeue_worker.py >/dev/null 2>&1 &
	echo "Done !" >> /tmp/webcrawler.log
elif [ "$1" = 'crawler' ]
then
	NUM_WORKERS=${2:-5}
	echo "Run $NUM_WORKERS crawlers ..." >> /tmp/webcrawler.log
	for (( i=0; i<=$NUM_WORKERS; i++ ))
	do
		echo "Run crawler $i ..." >> /tmp/webcrawler.log
		nohup python crawler.py >/dev/null 2>&1 &
	done
	echo "Done !" >> /tmp/webcrawler.log
fi

tail -F /tmp/webcrawler.log
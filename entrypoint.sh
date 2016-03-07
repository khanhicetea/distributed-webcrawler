#!/bin/bash

sed -i.bak -e "s/\$NUM_WORKERS/$NUM_WORKERS/" /etc/supervisor/conf.d/worker.conf

echo "Checking rethinkdb..." > /tmp/webcrawler.log
set -x
while ! curl rethink1:28015; do sleep 1; done

nohup /usr/bin/supervisord -n >>/tmp/webcrawler.log 2>&1 &
python main.py http://dmoz.org >>/tmp/webcrawler.log 2>&1 &

tail -F /tmp/webcrawler.log

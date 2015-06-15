#!/usr/bin/python
import sys
import time
import yaml
import rethinkdb as r
import gearman


parameter_file = open("parameters.yml", "r")
parameters = yaml.load(parameter_file)

rethink = r.connect(parameters['rethinkdb_server']['host'], parameters['rethinkdb_server']['port']).repl()
rethink.use(parameters['rethinkdb_server']['database'])

gm_client = gearman.GearmanClient(parameters['gearman_server']['hosts'])
gm_admin = gearman.GearmanAdminClient(parameters['gearman_server']['hosts'])

max_tasks = parameters['gearman_server']['max_tasks']

def num_dequeue_urls():
	gearman_status = gm_admin.get_status()
	for func in gearman_status:
		if func['task'] == "crawler":
			return int(max_tasks - func['queued'])
	return max_tasks

def main(argv):
    # Main code here
    print "I'm dequeue worker"

    url_queue_table = parameters['rethinkdb_server']['tables']['url_queue']
    dequeued_ids = []
    
    while True:
    	# Sleep 3 seconds
    	time.sleep(3)
    	num = num_dequeue_urls()
    	if num > 0:
    		del dequeued_ids[:]
    		cursor = r.table(url_queue_table).order_by(index='ts').limit(num).run(rethink)
    		for row in cursor:
    			dequeued_ids.append(row['id'])
    			gm_client.submit_job("crawler", str(row['url']), background=True)

    		if dequeued_ids:
	    		print "\t - Dequeue ", len(dequeued_ids), " urls"
	    		# Clean all dequeued url
	    		r.table(url_queue_table).filter(
	    			lambda row: r.expr(dequeued_ids).contains(row['id'])
	    		).delete().run(rethink)

if __name__ == "__main__":
    main(sys.argv)

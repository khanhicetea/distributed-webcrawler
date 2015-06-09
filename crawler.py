#!/usr/bin/python
import sys
import yaml
import rethinkdb as r
import gearman
import urllib2

parameter_file = open("parameters.yml", "r")
parameters = yaml.load(parameter_file)

rethink = r.connect(parameters['rethinkdb_server']['host'], parameters['rethinkdb_server']['port']).repl()
rethink.use(parameters['rethinkdb_server']['database'])
raw_result_table = parameters['rethinkdb_server']['tables']['raw_result']

gm_worker = gearman.GearmanWorker(parameters['gearman_server']['hosts'])

def task_listener_crawler(gearman_worker, gearman_job):
	url = gearman_job.data
	try:
		response = urllib2.urlopen(url)
		raw_data = response.read()
		r.table(raw_result_table).insert({'url': url, 'raw': raw_data}).run(rethink)
	except urllib2.HTTPError as e:
		pass
		
	return "ok"

def main(argv):
	# Main code here
	print "I'm crawler"

	gm_worker.register_task('crawler', task_listener_crawler)
	gm_worker.work()

	

if __name__ == "__main__":
	main(sys.argv)

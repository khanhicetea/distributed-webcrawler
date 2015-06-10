#!/usr/bin/python
import sys
import yaml
import rethinkdb as r
import gearman
import requests

parameter_file = open("parameters.yml", "r")
parameters = yaml.load(parameter_file)

rethink = r.connect(parameters['rethinkdb_server']['host'], parameters['rethinkdb_server']['port']).repl()
rethink.use(parameters['rethinkdb_server']['database'])
raw_result_table = parameters['rethinkdb_server']['tables']['raw_result']
crawler_headers = parameters['crawler_headers']
print crawler_headers
gm_worker = gearman.GearmanWorker(parameters['gearman_server']['hosts'])

def task_listener_crawler(gearman_worker, gearman_job):
	url = gearman_job.data
	print "Crawling ", url
	response = requests.get(url, crawler_headers)
	if response.status_code == 200:
		raw_data = response.text
		if response.encoding != 'utf8':
			raw_data = response.text.encode(response.encoding).decode('utf8')
		r.table(raw_result_table).insert({'url': url, 'raw': raw_data, 'status': 200}).run(rethink)
		return "ok"
	else:
		r.table(raw_result_table).insert({'url': url, 'status': response.status_code}).run(rethink)
	return "fail"

def main(argv):
	# Main code here
	print "I'm crawler"

	gm_worker.register_task('crawler', task_listener_crawler)
	gm_worker.work()

	

if __name__ == "__main__":
	main(sys.argv)

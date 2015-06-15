#!/usr/bin/python
import sys
import yaml
import rethinkdb as r
import gearman
import redis
from pybloomd import BloomdClient
import re
import urlparse
import requests
import urlnorm

parameter_file = open("parameters.yml", "r")
parameters = yaml.load(parameter_file)

rethink = r.connect(parameters['rethinkdb_server']['host'], parameters['rethinkdb_server']['port']).repl()
rethink.use(parameters['rethinkdb_server']['database'])
raw_result_table = parameters['rethinkdb_server']['tables']['raw_result']
redis_client = redis.Redis(parameters['redis_server']['host'])
gm_worker = gearman.GearmanWorker(parameters['gearman_server']['hosts'])
bloom_client = BloomdClient(parameters['bloomd_servers'])
url_frontier = bloom_client.create_filter('url_frontier')
linkregex = re.compile('<a\s*href=[\'|"](.*?)[\'"].*?>')
crawler_headers = parameters['crawler_headers']

def url_pre_norm(link, base):
	if link.startswith('/'):
		link = 'http://' + base[1] + link
	elif link.startswith('#'):
		link = 'http://' + base[1] + base[2] + link
	elif not link.startswith('http'):
		link = 'http://' + base[1] + '/' + link
	return link

def task_listener_crawler(gearman_worker, gearman_job):
	url = gearman_job.data
	url_frontier.add(url)
	urls = urlparse.urlparse(url)
	print "Crawling ", url
	response = requests.get(url, crawler_headers)
	if response.status_code == 200:
		raw_data = response.text
		if response.encoding != 'utf8':
			raw_data = response.text.encode(response.encoding).decode('utf8')
		r.table(raw_result_table).insert({'url': url, 'raw': raw_data, 'status': 200}).run(rethink)

		links = linkregex.findall(raw_data)
		for link in (links.pop(0) for _ in xrange(len(links))):
			pre_norm_url = url_pre_norm(link, urls)
			norm_url = urlnorm.norm(pre_norm_url)
			if url_frontier.add(norm_url):
				print "Add ", norm_url, " to redis queue"
				redis_client.rpush("urls:enqueued", norm_url)
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

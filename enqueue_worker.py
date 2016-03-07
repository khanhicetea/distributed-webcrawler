#!/usr/bin/python
import sys
import time
import yaml
import rethinkdb as r
import redis
import urlparse
import json

from reppy.cache import RobotsCache

robots = RobotsCache()
parameter_file = open("parameters.yml", "r")
parameters = yaml.load(parameter_file)

rethink = r.connect(parameters['rethinkdb_server']['host'], parameters['rethinkdb_server']['port']).repl()
rethink.use(parameters['rethinkdb_server']['database'])

redis_client = redis.Redis(parameters['redis_server']['host'])
crawl_delay = int(parameters['crawl_delay'])
user_agent = parameters['crawler_headers']['user-agent']

def is_polite(url, user_agent):
    allowed = False

    try:
        allowed = robots.allowed(url, user_agent)
    except:
        pass
    
    return allowed

def get_delay(url, user_agent):

    delay = None

    try:
        delay = robots.delay(url, user_agent)
    except:
        pass

    if not delay:
        delay = crawl_delay

    return delay


def main(argv):
    # Main code here
    print "I'm enqueue worker"

    url_queue_table = parameters['rethinkdb_server']['tables']['url_queue']

    while True:
        url = redis_client.lpop("urls:enqueued")

        if url:

            if not is_polite(url, user_agent):
                print 'Not polite to crawl... back off'
                time.sleep(0.3)
                continue

            delay = get_delay(url, user_agent)

            ts = int(time.time() / 60)
            urls = urlparse.urlparse(url)
            host_name = urls[1]
            host_raw = redis_client.get(host_name)
            host = json.loads(host_raw) if host_raw else {
                'n': 0,
                'ts': ts
            }
            if host['ts'] >= ts:
                if host['n'] >= delay:
                    host['ts'] = host['ts'] + 1
                    host['n'] = 1
                else:
                    host['n'] = host['n'] + 1
            else:
                host['ts'] = ts
                host['n'] = 0
            redis_client.set(host_name, json.dumps(host))
            r.table(url_queue_table).insert({'url': url, 'ts': host['ts']}).run(rethink)
        else:
            time.sleep(0.3)

if __name__ == "__main__":
    main(sys.argv)

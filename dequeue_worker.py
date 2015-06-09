#!/usr/bin/python
import sys
import yaml
import rethinkdb as r


parameter_file = open("parameters.yml", "r")
parameters = yaml.load(parameter_file)

rethink = r.connect(parameters['rethinkdb_server']['host'], parameters['rethinkdb_server']['port']).repl()
rethink.use(parameters['rethinkdb_server']['database'])

def main(argv):
    # Main code here
    print "I'm dequeue worker"

    url_queue_table = parameters['rethinkdb_server']['tables']['url_queue']

if __name__ == "__main__":
    main(sys.argv)

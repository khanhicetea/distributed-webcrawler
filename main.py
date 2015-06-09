#!/usr/bin/python
import sys
import time
import yaml
import rethinkdb as r


parameter_file = open("parameters.yml", "r")
parameters = yaml.load(parameter_file)

rethink = r.connect(parameters['rethinkdb_server']['host'], parameters['rethinkdb_server']['port']).repl()
rethink.use(parameters['rethinkdb_server']['database'])

def main(argv):
    # Main code here
    print "I'm manager :)"

    seed_url = "http://vnexpress.net/"
    if 1 in argv:
        seed_url = argv[1]

    url_queue_table = parameters['rethinkdb_server']['tables']['url_queue']
    r.table(url_queue_table).insert({'url': seed_url}).run(rethink)
    print "\tInserted the SEED URL"

    current_rows = 0
    result_table_name = parameters['rethinkdb_server']['tables']['indexed_result']

    while True:
        time.sleep(1)
        total_rows = r.table(result_table_name).count().run(rethink)
        if current_rows != total_rows:
            current_rows = total_rows
            print "\tTotal rows is ", total_rows

if __name__ == "__main__":
    main(sys.argv)

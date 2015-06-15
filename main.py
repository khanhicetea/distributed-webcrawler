#!/usr/bin/python
import sys
import time
import yaml
import rethinkdb as r


parameter_file = open("parameters.yml", "r")
parameters = yaml.load(parameter_file)

print "Connecting database ..."
rethink = r.connect(parameters['rethinkdb_server']['host'], parameters['rethinkdb_server']['port']).repl()
rethink_db = parameters['rethinkdb_server']['database']
url_queue_table = parameters['rethinkdb_server']['tables']['url_queue']
raw_result_table = parameters['rethinkdb_server']['tables']['raw_result']
indexed_result_table = parameters['rethinkdb_server']['tables']['indexed_result']
# Init database
db_list = r.db_list().run(rethink)
if rethink_db not in db_list:
    print "Init database ..."
    r.db_create(rethink_db).run(rethink)
    r.db(rethink_db).table_create(url_queue_table).run(rethink)
    r.db(rethink_db).table(url_queue_table).index_create('ts').run(rethink)
    r.db(rethink_db).table_create(raw_result_table).run(rethink)
    r.db(rethink_db).table_create(indexed_result_table).run(rethink)

rethink.use(rethink_db)

def main(argv):
    # Main code here
    print "I'm manager :)"

    seed_url = "http://vnexpress.net/"
    if 1 in argv:
        seed_url = argv[1]

    r.table(url_queue_table).insert({'url': seed_url, 'ts': 0}).run(rethink)
    print "\t- Inserted the SEED URL : ", seed_url

if __name__ == "__main__":
    main(sys.argv)

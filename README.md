# Distributed web-crawler based on Docker

## Introdution

This is a small web-crawler project used distributed architecture and based on Docker.
It also used cool OpenSource projects :
- [RethinkDB](http://rethinkdb.com/) 
- [Gearman Job Server](http://gearman.org/)
- [Redis](http://redis.io/)
- [Bloom Filter Server](https://github.com/armon/bloomd)

It's mainly built on Python Language, but you can use many others Languages (C, C++, Java, PHP, NodeJS, ...) to implement.

## Distributed Architecture
![Distributed Architecture of Web Crawler](http://i.imgur.com/dQkwLJF.png)

## Requirements

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Installation

Step 1 : Build docker image
```bash
git clone https://github.com/khanhicetea/distributed-webcrawler.git
cd distributed-webcrawler
docker-compose build
```

Step 2 : Run init containers
```bash
docker-compose up -d
```

Step 3 : Run crawlers
```bash
docker exec -it distributedwebcrawler_worker1_1 /entrypoint.sh crawler [number_of_crawlers]
```

## ENJOY !!!

- Go to : [http://YOUR_IP_ADDRESS:8080/](http://YOUR_IP_ADDRESS:8080/) to manage your RethinkDB database
- Go to : [http://YOUR_IP_ADDRESS:4731/](http://YOUR_IP_ADDRESS:4731/) to view Gearmand server status

## Credits

* [All contributors](https://github.com/khanhicetea/distributed-webcrawler/graphs/contributors)

## License

Licensed under the MIT License - see the [LICENSE](LICENSE) file
for details.

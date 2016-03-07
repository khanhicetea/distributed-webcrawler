FROM python:2.7

VOLUME /code
WORKDIR /code

ADD requirements.txt /code/

RUN apt-get -y update
RUN apt-get install -y openssh-server supervisor

RUN pip install -r requirements.txt
RUN git clone https://github.com/kiip/bloom-python-driver.git /tmp/bloom-python-driver
RUN cd /tmp/bloom-python-driver && python setup.py install

ADD entrypoint.sh /entrypoint.sh
RUN chmod 755 /entrypoint.sh

ENV NUM_WORKERS 1

COPY supervisord_config/* /etc/supervisor/conf.d/ 

ENTRYPOINT ["/entrypoint.sh"]

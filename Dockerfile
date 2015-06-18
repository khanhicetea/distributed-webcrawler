FROM python:2.7

VOLUME /code
WORKDIR /code

ADD requirements.txt /code/

RUN pip install -r requirements.txt
RUN git clone https://github.com/kiip/bloom-python-driver.git /tmp/bloom-python-driver
RUN cd /tmp/bloom-python-driver && python setup.py install

ADD entrypoint.sh /entrypoint.sh
RUN chmod 755 /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh", "master"]

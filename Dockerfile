FROM python:3.7.2

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY pip.conf /root/.pip/pip.conf
COPY . /usr/src/app/
RUN pip install -r /usr/src/app/requirements.txt && \
    chmod 777 /usr/src/app/run.sh

CMD [ "/bin/bash", "-c", "/usr/src/app/run.sh"]

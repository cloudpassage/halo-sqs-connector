FROM docker.io/halotools/python-sdk:ubuntu-16.04_sdk-1.0.5 as TESTER
MAINTAINER toolbox@cloudpassage.com

RUN pip install pytest

COPY app/ /app/

COPY requirements.txt /app/

RUN pip install -r /app/requirements.txt

RUN py.test /app

####

FROM docker.io/halotools/python-sdk:ubuntu-16.04_sdk-1.0.5
MAINTAINER toolbox@cloudpassage.com

ENV HALO_API_HOSTNAME=api.cloudpassage.com

RUN pip install pytest

COPY app/ /app/

COPY requirements.txt /app/

RUN pip install -r /app/requirements.txt

ENTRYPOINT /usr/bin/python /app/application.py

CMD ""

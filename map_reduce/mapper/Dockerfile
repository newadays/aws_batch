FROM python:3

ARG VERSION="1.0"

# Metadata
LABEL container.base.image="python:3"
LABEL software.version=${VERSION}
LABEL tags="mapreduce"


RUN pip install boto3 awscli

WORKDIR /

COPY mapper/requirements.txt /

RUN pip install --no-cache-dir -r /requirements.txt

ADD mapper/mapper.py /mapper.py

COPY mapper/lib /lib

ENTRYPOINT ["python", "mapper.py"]
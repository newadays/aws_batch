FROM python:3

ARG VERSION="1.0"

# Metadata
LABEL container.base.image="python:3"
LABEL software.version=${VERSION}
LABEL tags="mapreduce"

RUN apt-get update \
    && apt-get install -y bash
RUN pip install boto3 awscli

WORKDIR /

ADD requirements.txt /

RUN pip install --no-cache-dir -r /requirements.txt

ADD mapper.py /mapper.py

COPY lib /lib

ENTRYPOINT ["python", "mapper.py"]

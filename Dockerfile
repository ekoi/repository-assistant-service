FROM python:3.12.1-bookworm

ARG VERSION=0.2.8

RUN useradd -ms /bin/bash dans

USER dans
WORKDIR /home/dans
ENV PYTHONPATH=/home/dans/repository-assistant-service/src
ENV BASE_DIR=/home/dans/repository-assistant-service

COPY ./dist/*.* .

#
RUN mkdir -p ${BASE_DIR}  && \
    pip install --no-cache-dir *.whl && rm -rf *.whl && \
    tar xf repository_assistant_service-${VERSION}.tar.gz -C ${BASE_DIR} --strip-components 1 && \
    rm -rf ${BASE_DIR}/conf/* && rm -f repository_assistant_service-${VERSION}.tar.gz

WORKDIR ${BASE_DIR}

CMD ["python", "src/main.py"]
#CMD ["tail", "-f", "/dev/null"]
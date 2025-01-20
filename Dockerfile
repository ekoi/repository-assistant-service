FROM node:20.11-bookworm-slim AS node-image
FROM python:3.12.1-bookworm

ARG VERSION=0.2.12

RUN useradd -ms /bin/bash dans

COPY --from=node-image /usr/local/bin/node /usr/local/bin/
COPY --from=node-image /usr/local/lib/node_modules /usr/local/lib/node_modules
RUN ln -s ../lib/node_modules/npm/bin/npm-cli.js /usr/local/bin/npm \
    && ln -s ../lib/node_modules/npm/bin/npx-cli.js /usr/local/bin/npx

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

COPY start.sh .
#RUN chmod +x start.sh

#CMD ["python", "src/main.py"]
#CMD ["tail", "-f", "/dev/null"]
ENTRYPOINT ["/home/dans/repository-assistant-service/start.sh"]
FROM nikolaik/python-nodejs:python3.7-nodejs11
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

COPY Makefile /app/
COPY requirements.txt /app/
RUN make python_install

COPY package.json /app/
COPY package-lock.json /app/
RUN make npm_install

COPY .babelrc /app/
COPY webpack.config.js /app/
COPY static/ /app/static/
COPY generator /app/generator/

ENTRYPOINT bash -c "make build_static && make migrate && make start_server"

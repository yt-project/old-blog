FROM jfloff/alpine-python:2.7-slim

COPY ./requirements.txt /requirements.txt

RUN /entrypoint.sh \
  -r /requirements.txt \
  -b libgit2-dev \
  -b libffi-dev \
  -a git \
  -a libgit2 \
&& echo

RUN sed -e 's/flask.ext.babel/flask_babel/g' \
  -i /usr/lib/python2.7/site-packages/blohg/__init__.py

WORKDIR /app
COPY .git /app/.git
COPY blohg_converter.py /app/blohg_converter.py
COPY config.yaml /app/config.yaml
COPY content /app/content
COPY static /app/static
COPY templates /app/templates

EXPOSE 5000
CMD ["blohg", "runserver", "--no-debug", "-t", "0.0.0.0", "-p", "5000"]

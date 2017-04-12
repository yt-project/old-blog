FROM debian:sid

RUN groupadd -g 1000 fido && \
  useradd -m -g 1000 -G 1000 -u 1000 -s /bin/bash fido

RUN apt-get update -qy && \
  apt-get install -qy python-blinker python-docutils python-flask python-flask-babel \
    locales python-pygit2 python-hglib python-frozen-flask python-yaml \
    python-pygments python-setuptools python-click git && \
  apt-get clean && rm -rf /var/lib/apt/lists/*

RUN echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen && locale-gen
ENV LANG=en_US.UTF-8 LANGUAGE=en_US.UTF-8 LC_ALL=en_US.UTF-8

RUN cd /tmp && git clone https://github.com/rafaelmartins/blohg && \
  cd blohg/ && \
  sed -e 's/\(_external=\)True/\1False/' \
      -i blohg/views.py blohg/rst_parser/roles.py blohg/rst_parser/directives.py \
         blohg/templates/404.html && \
  python setup.py install && \
  cd /tmp && rm -rf /tmp/*

RUN chown fido:fido /srv
USER fido
RUN git clone https://github.com/yt-project/blog /srv/blog

WORKDIR /srv/blog
EXPOSE 5000
CMD ["blohg", "runserver", "--no-debug", "-t", "0.0.0.0", "-p", "5000"]

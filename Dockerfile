FROM debian:sid

RUN groupadd -g 1000 fido && \
  useradd -m -g 1000 -G 1000 -u 1000 -s /bin/bash fido

RUN apt-get update -qy && \
  apt-get install -qy wget unzip \
    python-blinker python-docutils python-flask python-flask-babel mercurial locales \
    python-frozen-flask python-yaml python-pygments python-setuptools python-click \
    python-hglib && \
  apt-get clean && rm -rf /var/lib/apt/lists/*

RUN echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen && locale-gen
ENV LANG=en_US.UTF-8 LANGUAGE=en_US.UTF-8 LC_ALL=en_US.UTF-8

RUN cd /tmp && wget --quiet https://github.com/rafaelmartins/blohg/archive/master.zip && \
  unzip -qq master.zip && cd blohg-master/ && \
  sed -e 's/\(_external=\)True/\1False/' \
      -i blohg/views.py blohg/rst_parser/roles.py blohg/rst_parser/directives.py \
         blohg/templates/404.html && \
  python setup.py install && cd /tmp && rm -rf blohg* *.zip

RUN chown fido:fido /srv

USER fido
RUN cd /srv && hg clone https://bitbucket.org/yt_analysis/blog

WORKDIR /srv/blog
EXPOSE 5000
CMD ["blohg", "runserver", "--no-debug", "-t", "0.0.0.0", "-p", "5000"]
